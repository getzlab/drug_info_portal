from operator import itemgetter
import os
from urllib.parse import urljoin
from dataclasses import dataclass, asdict
import requests


__SESSION_SEER = None
__ROOT_SEER_URL = "https://api.seer.cancer.gov"


class Error(Exception):
    pass


class RequestSEERError(Error):
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


@dataclass(init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=False)
class SeerResult:
    entry: str
    found_flag: bool = False
    alternate_name: str = ""
    abbreviation: str = ""
    category: str = ""
    drugs: str = ""
    name: str = ""
    histology: str = ""
    note: str = ""
    primary_site: str = ""
    radiation: str = ""
    subcategory: str = ""
    remarks: str = ""


def __set_session():
    global __SESSION_SEER
    if __SESSION_SEER is None:
        SEER_API_KEY = os.environ["SEER_API_KEY"]
        __SESSION_SEER = requests.Session()
        __SESSION_SEER.headers.update({"X-SEERAPI-Key": SEER_API_KEY})


def __get(methodCall: str, rootURL: str = None, **kwargs):
    __set_session()
    if rootURL is None:
        rootURL = __ROOT_SEER_URL
    return __SESSION_SEER.get(urljoin(rootURL, methodCall), **kwargs)


def get_rx_id(entry: str, vertion: str = "latest"):
    """
    Returns list of Rx entries from Antineoplastic drug database
    Sends GET https://api.seer.cancer.gov/rest/rx/{version} requests
    return id with highest match score
    Args:
        entry (str): Entry to search for
        vertion (str, optional): rx vertion. Defaults to "latest".

    Raises:
        RequestError:

    Returns:
        str: id with with matching name or highest score relevence score
    """
    methodCall = f"rest/rx/{vertion}"
    params = {"type": "DRUG", "q": entry}
    res = __get(methodCall, params=params)
    if res.status_code != 200:
        raise RequestSEERError(res, 200)
    data = res.json()
    if data["total"] < 1:
        return
    # Match by name
    matchname = [r for r in data["results"] if r["name"].lower() == entry.lower()]
    if len(matchname) > 0:
        return matchname[0]["id"]
    # relevence score
    results = sorted(data["results"], key=itemgetter("score"), reverse=True)
    return results[0]["id"]


def get_rx_response(rxId, vertion: str = "latest"):
    if rxId is None:
        return
    methodCall = "rest/rx/{0}/id/{1}".format(vertion, rxId)
    res = __get(methodCall)
    if res.status_code != 200:
        raise RequestSEERError(res, 200)
    return res


def get_rx_info(entry: str, vertion: str = "latest"):
    dataSEER = SeerResult(entry)
    try:
        idx = get_rx_id(entry, vertion=vertion)
    except RequestSEERError:
        return asdict(dataSEER)
    try:
        response = get_rx_response(idx, vertion=vertion)
    except RequestSEERError:
        return asdict(dataSEER)

    if response is None:
        return asdict(dataSEER)

    data = response.json()
    dataSEER.found_flag = True
    if "alternate_name" in data:
        dataSEER.alternate_name = ", ".join(data["alternate_name"])
    if "abbreviation" in data:
        dataSEER.abbreviation = ", ".join(data["abbreviation"])
    if "category" in data:
        dataSEER.category = ", ".join(data["category"])
    if "drugs" in data:
        dataSEER.drugs = ", ".join(data["drugs"])
    if "name" in data:
        dataSEER.name = data["name"]
    if "primary_site" in data:
        dataSEER.primary_site = ", ".join(data["primary_site"])
    if "radiation" in data:
        dataSEER.radiation = data["radiation"]
    if "remarks" in data:
        dataSEER.remarks = " ".join(data["remarks"].split("\n"))
    if "subcategory" in data:
        dataSEER.subcategory = ", ".join(data["subcategory"])
    return asdict(dataSEER)


if __name__ == "__main__":
    pass