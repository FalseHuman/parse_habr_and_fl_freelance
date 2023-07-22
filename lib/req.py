from os import path

import requests

from .gen_filename import gen_filename_by_url


def get_response(url: str, filter_url: str = None, fl_page=False) -> requests.Response:
    if filter_url:
        if '?' in url:
            url += f'&{filter_url}'
        else:
            url += f'?{filter_url}'

    # print(f'получена страница: {url}')
    if fl_page:
        cookies = {
            '__ddg1_': 'MLcFNpPE1QarAAIyToFY',
            '_ym_uid': '1689778560949153560',
            '_ym_d': '1689778560',
            'analytic_id': '1689778563285183',
            'mindboxDeviceUUID': '17ea8707-c2f6-4af8-b239-0fb44aa7fc3d',
            'directCrm-session': '%7B%22deviceGuid%22%3A%2217ea8707-c2f6-4af8-b239-0fb44aa7fc3d%22%7D',
            'new_pf0': '1',
            'new_pf10': '1',
            'hidetopprjlenta': '0',
            'cookies_accepted': '1',
            '_tm_lt_sid': '1689780583501.932843',
            '_gid': 'GA1.2.395414171.1689922875',
            'carrotquest_device_guid': 'c3384b0e-4cca-406d-aa25-2ae64106452e',
            'id': '8241387',
            'name': 'emilkhazioff',
            'pwd': 'e6cad45f05734fdec2caef06bc44e43f',
            'PHPSESSID': 'v09ukI2UIUWn4jzNYHmLbSAsaWLXyTYbJ6GnCYrK',
            'user_device_id': 'pkoi1a0s44xg83r49lnusovsv8v2pxrc',
            'carrotquest_uid': '1491555967022664914',
            'carrotquest_auth_token': 'user.1491555967022664914.53881-61bf205fd2adedf70dea3c48bc.dd8f7c4f70cea6cbaf23197e691fbf8b1bb9724fb5468b22',
            'is_hide_bonus_plate': 'true',
            'ue_sso_token': '3hRs1vqExVfGdQ8V786H9HuSDpYIKlF8ojD4dgYasfhJCs49rBMT9q%252FolXb3a5SB%252F2l33kiKdrNYpiBJv0WMe8dbpGRosUL1XyHRpjJCLJ%252BWVsl4NT9cgx55g5bastnAwuyfwzF4zCppe0SpL4LBG0Ff5tQ%252FjMPEunTQTfY7dfdCEwu60JzYq9oaR%252FWyWRc9%252BgKzyfjfZwuJ72pt1AfgyqWybSLqfgc4uu0NAw1ouP%252FVPXORj4CN9sfL7o5aZhIClBpSXSmrbFLsRcbkpEeLOTmE%252FfYvTZr17kC5qXzSdO3ShqHrqJHRV6hCz1cDLWOJ0BbgIT4sQrpgtVs%252F8ZxKNMc9TMi6g7FihnaMHctXD%252B0Aw7du8%252BOkmby1DnQjkif%252FisjtwN%252BVK9ET1KtIuZRVUxRGzigOP1ksdEprO1A35cWqTZg9VioT0TL2dBzYXFy%252FwX2U7UgzKmCnnFu90jey%252BZqIepU7KjxJyM4%252BllxvjxV9EvkpNcyWrp2QSvgCsOOCrhQ3ttKyg%252Fhe2TELzOso0gJsBoefeA85oWR%252FoCD93Bg16wxL2aHM8wKLSBLMQTAE',
            'mobapp': '1690022696',
            'XSRF-TOKEN': 'AiGWRKDorBg0XmLIwUWbXdvwXQR7bC01BpnOarDO',
            '_ym_isad': '2',
            '_ga_cid': '949861448.1689778560',
            '_ym_visorc': 'w',
            'uechat_3_first_time': '1690022699767',
            'carrotquest_realtime_services_transport': 'wss',
            'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE2OTAwMjYzMDAsImlhdCI6MTY5MDAyMjcwMCwianRpIjoiZTg3MzMyZjBkYjU5NDBmYmE2MmYzMDM2N2Q1NjZlNzYiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTY5MDAyMjcwMCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjUzODgxLiR1c2VyX2lkOjE0OTE1NTU5NjcwMjI2NjQ5MTQiXSwiYXBwX2lkIjo1Mzg4MSwidXNlcl9pZCI6MTQ5MTU1NTk2NzAyMjY2NDkxNH0.TFAhhahFwqfbvX0RQ6kgeS602kVBV90XJhf3u1VT6CE',
            'uechat_3_disabled': 'true',
            'uechat_3_mode': '0',
            '_gat': '1',
            'uechat_3_pages_count': '6',
            'carrotquest_session': 'yuhvdysvq7umo7h6on9vpetfiao0695c',
            'carrotquest_session_started': '1',
            '_ga': 'GA1.1.949861448.1689778560',
            '_ga_RD9LL0K106': 'GS1.1.1690022697.5.1.1690024252.0.0.0',
        }
        headers = {
            'authority': 'www.fl.ru',
            'accept': 'application/json',
            'accept-language': 'ru,en;q=0.9,la;q=0.8,es;q=0.7,zh;q=0.6,bg;q=0.5',
            # 'cookie': '__ddg1_=MLcFNpPE1QarAAIyToFY; _ym_uid=1689778560949153560; _ym_d=1689778560; analytic_id=1689778563285183; mindboxDeviceUUID=17ea8707-c2f6-4af8-b239-0fb44aa7fc3d; directCrm-session=%7B%22deviceGuid%22%3A%2217ea8707-c2f6-4af8-b239-0fb44aa7fc3d%22%7D; new_pf0=1; new_pf10=1; hidetopprjlenta=0; cookies_accepted=1; _tm_lt_sid=1689780583501.932843; _gid=GA1.2.395414171.1689922875; carrotquest_device_guid=c3384b0e-4cca-406d-aa25-2ae64106452e; id=8241387; name=emilkhazioff; pwd=e6cad45f05734fdec2caef06bc44e43f; PHPSESSID=v09ukI2UIUWn4jzNYHmLbSAsaWLXyTYbJ6GnCYrK; user_device_id=pkoi1a0s44xg83r49lnusovsv8v2pxrc; carrotquest_uid=1491555967022664914; carrotquest_auth_token=user.1491555967022664914.53881-61bf205fd2adedf70dea3c48bc.dd8f7c4f70cea6cbaf23197e691fbf8b1bb9724fb5468b22; is_hide_bonus_plate=true; ue_sso_token=3hRs1vqExVfGdQ8V786H9HuSDpYIKlF8ojD4dgYasfhJCs49rBMT9q%252FolXb3a5SB%252F2l33kiKdrNYpiBJv0WMe8dbpGRosUL1XyHRpjJCLJ%252BWVsl4NT9cgx55g5bastnAwuyfwzF4zCppe0SpL4LBG0Ff5tQ%252FjMPEunTQTfY7dfdCEwu60JzYq9oaR%252FWyWRc9%252BgKzyfjfZwuJ72pt1AfgyqWybSLqfgc4uu0NAw1ouP%252FVPXORj4CN9sfL7o5aZhIClBpSXSmrbFLsRcbkpEeLOTmE%252FfYvTZr17kC5qXzSdO3ShqHrqJHRV6hCz1cDLWOJ0BbgIT4sQrpgtVs%252F8ZxKNMc9TMi6g7FihnaMHctXD%252B0Aw7du8%252BOkmby1DnQjkif%252FisjtwN%252BVK9ET1KtIuZRVUxRGzigOP1ksdEprO1A35cWqTZg9VioT0TL2dBzYXFy%252FwX2U7UgzKmCnnFu90jey%252BZqIepU7KjxJyM4%252BllxvjxV9EvkpNcyWrp2QSvgCsOOCrhQ3ttKyg%252Fhe2TELzOso0gJsBoefeA85oWR%252FoCD93Bg16wxL2aHM8wKLSBLMQTAE; mobapp=1690022696; XSRF-TOKEN=AiGWRKDorBg0XmLIwUWbXdvwXQR7bC01BpnOarDO; _ym_isad=2; _ga_cid=949861448.1689778560; _ym_visorc=w; uechat_3_first_time=1690022699767; carrotquest_realtime_services_transport=wss; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE2OTAwMjYzMDAsImlhdCI6MTY5MDAyMjcwMCwianRpIjoiZTg3MzMyZjBkYjU5NDBmYmE2MmYzMDM2N2Q1NjZlNzYiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTY5MDAyMjcwMCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjUzODgxLiR1c2VyX2lkOjE0OTE1NTU5NjcwMjI2NjQ5MTQiXSwiYXBwX2lkIjo1Mzg4MSwidXNlcl9pZCI6MTQ5MTU1NTk2NzAyMjY2NDkxNH0.TFAhhahFwqfbvX0RQ6kgeS602kVBV90XJhf3u1VT6CE; uechat_3_disabled=true; uechat_3_mode=0; _gat=1; uechat_3_pages_count=6; carrotquest_session=yuhvdysvq7umo7h6on9vpetfiao0695c; carrotquest_session_started=1; _ga=GA1.1.949861448.1689778560; _ga_RD9LL0K106=GS1.1.1690022697.5.1.1690024252.0.0.0',
            'dnt': '1',
            'referer': 'https://www.fl.ru/projects/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2562 Yowser/2.5 Safari/537.36',
            'x-csrf-token': 'AiGWRKDorBg0XmLIwUWbXdvwXQR7bC01BpnOarDO',
            'x-xsrf-token': 'AiGWRKDorBg0XmLIwUWbXdvwXQR7bC01BpnOarDO',
        }
    else:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
    try:
        if fl_page:
            response = requests.get(url, cookies=cookies, headers=headers)
        else:
            response = requests.get(url, headers=headers)
    except Exception:
        print('page is not found')
        exit()

    return response
