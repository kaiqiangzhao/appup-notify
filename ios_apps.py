#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import os
import requests
import json
import config


class IosApps:
    def get_apps_ids(self, apps_path):
        files = os.listdir(apps_path)
        apps_ids = []
        for file in files:
            app_id = file.split(".")[0]
            apps_ids.append(app_id)
        return apps_ids

    def get_app_info_itunes(self, app_id=989673964):
        base_url = "https://itunes.apple.com/lookup"
        params = {
            "id": app_id,
            "country": "cn",
            "entity": "software"
        }
        data = requests.get(url=base_url, params=params)
        json_data = json.loads(data.text)
        app = json_data.get("results")[0] if json_data.get("resultCount") >= 0 else {}
        return app

    def get_app_info_local(self, app_id, apps_path):
        full_path = os.path.join(apps_path, "{}.txt".format(app_id))
        with open(full_path, 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        app = json_data.get("results")[0] if json_data.get("resultCount") >= 0 else {}
        return app

    def get_app_version(self, app):
        # 数据抽取
        version = app.get("version", "0")
        return version

    def format_file_size(self, file_size_bytes):
        file_size_str = "0"
        if file_size_bytes >= 1024 * 3:
            file_size_str = "{}G".format(round(file_size_bytes / 1024 ** 3, 2))
        elif file_size_bytes >= 1024 * 3:
            file_size_str = "{}M".format(round(file_size_bytes / 1024 ** 2, 2))
        return file_size_str

    def compare_apps_version(self, app_id, apps_path):
        app_info_itunes = self.get_app_info_itunes(app_id)
        app_info_local = self.get_app_info_local(app_id, apps_path)
        app_version_now = self.get_app_version(app_info_itunes)
        app_version_before = self.get_app_version(app_info_local)
        if app_version_now > app_version_before:
            self.show_update_content(app_info_itunes, app_info_local)

    def show_update_content(self, app_info_itunes, app_info_local):
        track_id = app_info_itunes.get("trackId")
        version = app_info_itunes.get("version", "0")
        track_name = app_info_itunes.get("trackName")
        file_size_bytes = int(app_info_itunes.get("fileSizeBytes"))
        file_size_bytes_local = int(app_info_local.get("fileSizeBytes"))
        release_notes = app_info_itunes.get("releaseNotes")
        app_version_before = self.get_app_version(app_info_local)

        # 文件大小
        file_size_str = self.format_file_size(file_size_bytes)
        file_size_str_local = self.format_file_size(file_size_bytes_local)
        # print(track_id)
        print("应用名:{}".format(track_name))
        print("上一版本号:{}, 当前版本号{}".format(app_version_before, version))
        print("上一版本应用大小{}, 当前版本应用大小{}".format(file_size_str, file_size_str_local))
        print("本次更新内容:")
        print(release_notes)


if __name__ == '__main__':
    ios_apps = IosApps()
    ios_apps_path = config.ios_apps_path
    app_ids = ios_apps.get_apps_ids(ios_apps_path)
    for app_id in app_ids:
        ios_apps.compare_apps_version(app_id, ios_apps_path)


