# BJUT_Always_Online

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)![build: success](https://img.shields.io/badge/Build-success-green.svg)


README [English](#English) | [中文](#中文)

## English
### Introduction

BJUT_Always_Online is a test project based on Python, it is used to auto-login the campus network (**both for wired network and wireless network**) with a bunch of accounts in Beijing University of Technology.


### Features

+ Time heartbeat packet, avoid kicked by the gateway.
+ Cross-platform, based on Python.
+ Detect the rest of traffic flows.
+ Set the upper limit of traffic flows, and change account automatically.
+ Auto reset the index of account list at the start of each month.
+ Set backup account to keep online and ignore the limitation of traffic flows (this may produce network traffic cost).

### Usage

1. Create `accounts.txt` and `backupac.txt` as the sample formats.
2. Execute `python online.py`.

## 中文
### 介绍

BJUT_Always_Online 是一个基于 Python 语言开发的项目，它是一个测试项目，用于实现位于北京工业大学校园网内的主机自动登录城市热点的 **无线和有线网络** 认证系统，实现服务器持续在线。

### 特性

+ 定时发送心跳包，避免被网关踢下线。
+ 跨平台使用，支持 Windows、Linux、Mac OS 等一切安装了 Python 的操作系统。
+ 账号剩余流量监测。
+ 限制账号使用流量上限，并自动更换账号。
+ 月初自动重置账号列表。
+ 设置应急账号，无视流量限制而保持在线（可能会产生费用）。

### 使用

1. 建立 `accounts.txt` 和 `backupac.txt`，参照 sample 中的格式填写网关账号密码。
2. 执行 `python online.py`。