import requests
from itertools import islice
import os
from urllib.parse import urlencode, urljoin


__SESSION_FDA = None
__ROOT_FDA_URL = "https://api.fda.gov/drug/ndc.json"


class Error(Exception):
    pass


class RequestFDAError(Error):
    def __init__(self, response: requests.Response, expectedCode: int) -> None:
        """Raise if status code of response not

        Args:
            response (requests.Response): [description]
            expectedCode (int): [description]. Expected status code
        """
        self.response = response
        self.expectedCode = expectedCode
        self.message = "Status code is not {}".format(self.expectedCode)
        super().__init__(self.message)

    def __str__(self) -> str:
        errStr = "Status Code {0} is not {1} URL -> {2}".format(
            self.response.status_code, self.expectedCode, self.response.url
        )
        return errStr


def __set_session():
    global __SESSION_FDA
    if __SESSION_FDA is None:
        __SESSION_FDA = requests.Session()
        __SESSION_FDA.headers.update(
            {"Authorization": f"Basic {os.environ['FDA_API_KEY']}"}
        )


def __get(methodCall: str, rootURL: str = None, **kwargs):
    __set_session()
    if rootURL is None:
        rootURL = __ROOT_FDA_URL
    return __SESSION_FDA.get(urljoin(rootURL, methodCall), **kwargs)


def __prep_entry(entry: str):
    mapDict = {ord(ch): None for ch in "\"'"}
    e = entry.strip().translate(mapDict).lower().capitalize()
    return e.translate({ord(" "): "+"})


def get_fda_info(drugName: str):
    """Get info from openFDA
        https://api.fda.gov/drug/ndc.json
    Args:
        drugName (str): drug name

    Raises:
        RequestFDAError: if cannot get info

    Returns:
        dict: info
    """
    params = {"search": "", "limit": 1}
    entry = __prep_entry(drugName)
    searchStr = '(generic_name.exact:"{0}"+brand_name.exact:"{0}")'.format(entry)
    params["search"] = searchStr
    paramsStr = urlencode(params, safe="+:")
    res = __get(methodCall="", params=paramsStr)
    if res.status_code != 200:
        raise RequestFDAError(res, 200)
    data = res.json()
    # check if search found any results
    if "meta" not in data:
        return
    if data["meta"]["results"]["total"] < 1:
        return

    outDict = {
        "entry": drugName,
        "brand_name": "",
        "generic_name": "",
        "active_ingredients": "",
        "labeler_name": "",
        "pharm_class": "",
        "route": "",
    }
    results = data["results"][0]
    if "brand_name" in results:
        outDict["brand_name"] = results["brand_name"].strip()
    if "generic_name" in results:
        outDict["generic_name"] = results["generic_name"].strip()
    if "active_ingredients" in results:
        outDict["active_ingredients"] = ",".join(
            x["name"].strip() for x in results["active_ingredients"]
        )
    if "labeler_name" in results:
        outDict["labeler_name"] = results["labeler_name"].strip()
    if "pharm_class" in results:
        outDict["pharm_class"] = ",".join(x.strip() for x in results["pharm_class"])
    if "route" in results:
        outDict["route"] = ",".join(x.strip() for x in results["route"])
    return outDict


if __name__ == "__main__":
    pass