import requests

def get_access_token(sp_dc_cookie: str):
    headers = {"Cookie": f"sp_dc={sp_dc_cookie}"}
    url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    r = requests.get(url, headers=headers)
    if r.status_code == 401:
        raise Exception("Invalid cookie.")
    return r.json()["accessToken"]

def get_friend_activity(access_token: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "App-platform": "WebPlayer"
    }
    url = "https://spclient.wg.spotify.com/presence-view/v1/buddylist"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json().get("friends", [])
