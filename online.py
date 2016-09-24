# coding=utf-8
import requests
import linecache
import time
from html.parser import HTMLParser

# this global variable is used to avoid SSL cert verify fail when fiddler is used
fiddler_ssl = False


def if_overused():
    class HtmlPar(HTMLParser):
        ct_script = 0
        flg_script = False
        used_data = ""

        def handle_starttag(self, tag, attrs):
            if len(attrs) != 0 and len(attrs[0]) != 0:
                if tag == "script" and attrs[0][1] == "JavaScript":
                    HtmlPar.ct_script = HtmlPar.ct_script + 1
                    HtmlPar.flg_script = True

        def handle_endtag(self, tag):
            if tag == "script":
                HtmlPar.flg_script = False

        def handle_data(self, data):
            if HtmlPar.flg_script and HtmlPar.ct_script == 1:
                # get used traffic
                str_idx_s = data.index("';flow='") + 8
                str_idx_e = data.index("';fsele=", str_idx_s)
                HtmlPar.used_data = data[str_idx_s:str_idx_e].rstrip()

    html_url = "https://lgn.bjut.edu.cn/"
    try:
        html_res = requests.get(html_url, verify=not fiddler_ssl)
        html_res.encoding = "GB2312"
    except:
        print_log("Failed to get login page. Exiting.")
        exit()
    html_par = HtmlPar()
    # print(html_res.text)
    if not is_online(html_res):
        # not logged in
        return -1
    else:
        html_par.flg_is_online = True
        html_par.feed(html_res.text)
        print_log(html_par.used_data + '\t' + str(int(int(html_par.used_data) / (8 * 1024 * 1024) * 100)) + '%')
        if int(html_par.used_data) / (8 * 1024 * 1024) < 0.9:
            # not overused
            return 0
        else:
            # used over 90 percent
            return 1


def get_available_account():
    f_index = open("index.txt")
    index = int(f_index.readline().strip('\n'))
    f_index.close()
    try:
        u_acc = linecache.getline("accounts.txt", index).strip('\n').split(',')
        return u_acc
    except:
        print_log("accounts used up")
        return 1


def renew_index():
    f_index = open("index.txt")
    index = int(f_index.readline().strip('\n'))
    f_index.close()
    f_index = open("index.txt", "w")
    f_index.write(str(index + 1))
    f_index.close()
    return 0


def is_online(html_res):
    class HtmlPar(HTMLParser):
        flg_title = False
        flg_success = True

        def handle_starttag(self, tag, attrs):
            if tag == 'title':
                HtmlPar.flg_title = True

        def handle_endtag(self, tag):
            if tag == 'title':
                HtmlPar.flg_title = False

        def handle_data(self, data):
            if HtmlPar.flg_title and data[0:11] == "北京工业大学上网登录窗":
                # not logged in
                HtmlPar.flg_success = False

    html_par = HtmlPar()
    html_par.feed(html_res.text)
    return html_par.flg_success


def is_success(html_res):
    class HtmlPar(HTMLParser):
        flg_title = False
        flg_success = False

        def handle_starttag(self, tag, attrs):
            if tag == 'title':
                HtmlPar.flg_title = True

        def handle_endtag(self, tag):
            if tag == 'title':
                HtmlPar.flg_title = False

        def handle_data(self, data):
            if HtmlPar.flg_title and data == "登录成功窗":
                HtmlPar.flg_success = True

    html_par = HtmlPar()
    html_par.feed(html_res.text)
    return html_par.flg_success


def logout():
    html_url = "https://lgn.bjut.edu.cn/F.html"
    try:
        requests.get(html_url, verify=not fiddler_ssl)
    except:
        print_log("No need to logout or logout err.")
        return 1
    print_log("Logged out.")
    return 0


def login():
    back_account = False
    while 1:
        account = get_available_account()
        if account == 1:
            print_log("Using backup account.")
            f_bkac = open("backupac.txt")
            account = f_bkac.readline().strip('\n').split(',')
            f_bkac.close()
            back_account = True

        print_log("Logging in " + account[0])
        html_values = {
            'DDDDD': account[0],
            'upass': account[1],
            'v46s': '1',
            '0MKKey': ''
        }
        html_url = "https://lgn.bjut.edu.cn/"
        html_res = None
        try:
            html_res = requests.post(html_url, data=html_values, verify=not fiddler_ssl)
            html_res.encoding = "GB2312"
        except:
            print_log("Could not open login page, exiting...")
            exit()

        # check login result
        if is_success(html_res):
            # login successfully
            print_log("Logged in. Checking traffic.")
            traffic_status = if_overused()
            if traffic_status == 0 or back_account == True:
                # login success
                print_log("Traffic enough.")
                return back_account
            elif traffic_status == -1:
                # not logged in
                print_log("Not logged in, try next.")
            elif traffic_status == 1:
                # overused
                print_log("Traffic used over 90%, try next.")
                logout()
            renew_index()  # index the next account
        else:
            # login not success
            print_log("Login failure, retry.")


def reset_index():
    f_index = open("index.txt", "w")
    f_index.write("1\n")
    f_index.close()


def print_log(content):
    print(content)
    f_log = open("log.txt", "a")
    f_log.write(time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + str(content) + '\n')
    f_log.close()
    return


if __name__ == "__main__":
    # when accounts are used up, backup account will be put in use.
    is_back_account = False

    # loop starts
    while 1:
        print_log("Checking traffic...")
        status = if_overused()
        if status == 0 or is_back_account == True:
            print_log("Fine")
        else:
            if status == -1:
                print_log("Offline. Log in.")
            elif status == 1:
                print_log("Traffic used over 90%, changing account...")
                logout()
                renew_index()
            is_back_account = login()

        # reset index every month
        t_time = time.localtime(time.time())
        if t_time.tm_mday == 1 and t_time.tm_hour == 0 and t_time.tm_min == 10:
            reset_index()

        time.sleep(60)
