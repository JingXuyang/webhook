# -*- coding:UTF-8 -*-
import yaml
import os
import subprocess
import time
import logging

# open file
with open("./project_config.yaml", "r") as f:
    CONFIG_DATA = yaml.load(f.read())


def init_logging():
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关

    # 第二步，创建一个handler，用于写入日志文件
    request_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_path = os.path.dirname(__file__)
    logfile = "{path}/Logs/{filename}.log".format(path=log_path, filename=request_time)
    file_handler = logging.FileHandler(logfile, mode='w')
    file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)

    # 第四步，将logger添加到handler里面
    logger.addHandler(file_handler)

    return logger


def verify_token(project_name, token):
    for info in CONFIG_DATA:
        if project_name == info.get("project"):
            if token == info.get("token"):
                return True
    return False


def pull(request, logger):
    for info in CONFIG_DATA:
        project_name = request.json.get("repository").get("name")
        if info.get("project") == project_name:
            path = info.get("path")
            if os.path.exists(path):
                git_ssh_url = request.json.get("repository").get("git_ssh_url")
                target = path.split("/")[-1]
                parent_path = os.path.dirname(path)
                print parent_path, target
                # subprocess.call("cd {path} && chmod -R 777 {target}".format(path=parent_path, target=target), shell=True)
                #
                subprocess.call("cd {} && git config --global core.autocrlf true".format(path), shell=True)
                set_url = subprocess.call("cd {path} && git remote set-url origin {url}".format(path=path, url=git_ssh_url), shell=True)
                if set_url == 0:
                    retcode = subprocess.call("cd {} && git pull".format(path), shell=True)
                    if retcode == 0:
                        commits = request.json.get("commits")
                        logger.info(">>>>>>>>>>>>>>>>>>>>>>>> Pull")
                        logger.info(u'  提交内容:  {}'.format(commits[0].get("message")))
                        logger.info(u'  修改文件:  {}'.format("; ".join(commits[0].get("modified"))))
                        logger.info("       结果: Successful.")
                    else:
                        logger.info("       结果: [{}] Git Pull Error.".format(project_name))
                else:
                    logger.info("       结果: [{}] 切换协议失败.".format(project_name))
    return True


