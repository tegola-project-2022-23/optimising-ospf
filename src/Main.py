import paramiko

from Host import Host
from Interface import Interface
import configparser
import json
import numpy as np
import requests
import telnetlib

class Main:



    def __init__(self):
        np.set_printoptions(suppress=True)
        config = configparser.ConfigParser()
        config.read_file(open(r'config.ini'))

        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": config.get("credentials", "username"),
                "password": config.get("credentials", "password")
            },
            "id": 1,
            "auth": None
        }

        request = requests.post(config.get("config", "api_url"), json=data)

        self.NUM_VALUES = config.get("config", "num_of_values")
        self.ITEM_IDS = json.load(open(r"hosts.json"))
        self.AUTH_TOKEN = request.json()["result"]
        self.SSH_PASSWORD = config.get("credentials", "ssh_password")
        self.API_URL = config.get("config", "api_url")
        self.hosts = []
        self.hosts_dict = {}
        self.demand_matrix = np.zeros(shape=(2, 2))     # 2x2 Matrix for the existing topology.
        self.current_ospf_cost = {}

    def run(self):
        self.get_zabbix_data()
        for host in self.hosts:
            print(host)
        self.generate_demand_matrix()
        self.zabbix_cleanup()

        self.update_cost()

    def get_current_ospf_cost(self):
        for host in self.hosts:
            ssh = paramiko.SSHClient()
            ssh.connect(host.ip, username="tegola", password=self.SSH_PASSWORD)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("hostname")
            print(ssh_stdout.readlines())

            ssh.close()

    def update_cost(self):
        # Update Cor
        cor = self.hosts_dict.get("cor")
        # cmd = 'vtysh -c "echo -e `show interface\nshow ip route`"'
        cmd = "hostname"
        self.exe_ssh_cmd(cor.ip, cmd)

        ssh = self.hosts_dict.get("ssh")
        cmd = "hostname"
        self.exe_ssh_cmd(ssh.ip, cmd)

        mhi = self.hosts_dict.get("mhi")
        cmd = "hostname"
        self.exe_ssh_cmd(mhi.ip, cmd)

        smo = self.hosts_dict.get("smo")
        cmd = "hostname"
        self.exe_ssh_cmd(smo.ip, cmd)
    def exe_ssh_cmd(self, ip, cmd):
        ssh = paramiko.SSHClient()
        ssh.connect(ip, username="tegola", password=self.SSH_PASSWORD)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        print(ssh_stdout.readlines())
        ssh.close()

    def get_zabbix_data(self):
        for origin in self.ITEM_IDS:
            host = Host(origin, self.ITEM_IDS.get(origin).get("id"), self.ITEM_IDS.get(origin).get("ip"))

            for destination in self.ITEM_IDS.get(origin):
                if destination == "id" or destination == "ip":
                    continue

                interface = Interface(origin, destination, self.ITEM_IDS.get(origin).get(destination).get("id"))
                sent_request = requests.post(self.API_URL, json=self.create_json(
                    self.ITEM_IDS.get(origin).get(destination).get("sent")))
                received_request = requests.post(self.API_URL, json=self.create_json(
                    self.ITEM_IDS.get(origin).get(destination).get("received")))

                sent_json = sent_request.json()
                received_json = received_request.json()

                print(sent_json)

                for sent_value, received_value in zip(sent_json["result"], received_json["result"]):
                    interface.bits_sent.append(int(sent_value["value"]))
                    interface.bits_received.append(int(received_value["value"]))

                host.interfaces.append(interface)
                host.interface_dict[interface.destination] = interface

            self.hosts.append(host)
            self.hosts_dict[host.name] = host

    def create_json(self, item_id):
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 3,
                "itemids": item_id,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": self.NUM_VALUES
            },
            "auth": self.AUTH_TOKEN,
            "id": 1
        }

        return data


    # @staticmethod
    # def update_cor_costs(host):
    #     count = 0
    #     while count < 10:
    #
    #
    #
    # def update_ssh_costs(self):
    #     pass

    # IDs are as follows:
    # SSH: 0
    # COR: 1
    # SMO: 2
    # MHI: 3
    def generate_demand_matrix(self):

        interface_matrix = [["", ""], ["", ""]]

        for host in self.hosts:
            if host.host_id == 0 or host.host_id == 1:
                for interface in host.interfaces:
                    if interface.destination_id == 0:
                        continue

                    self.demand_matrix[host.host_id][interface.destination_id-2] = interface.get_average_bits_sent()
                    interface_matrix[host.host_id][interface.destination_id-2] = f"{host.name} -> {interface.destination}"

        print(self.demand_matrix)
        print(interface_matrix)

    def zabbix_cleanup(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": [],
            "id": 1,
            "auth": self.AUTH_TOKEN
        }

        req = requests.post(self.API_URL, json=data)
        print(f"Logout: {req.json()['result']}")


if __name__ == "__main__":
    m = Main()
    m.run()
