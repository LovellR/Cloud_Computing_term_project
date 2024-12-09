import boto3

def create_security_group(group_name, description, vpc_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_security_group(GroupName=group_name, Description=description, VpcId=vpc_id)
        print("Created Security Group:", response)
    except Exception as e:
        print(f"Error creating Security Group: {e}")

def describe_security_groups():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_security_groups()
        for group in response['SecurityGroups']:
            print(f"Group Name: {group['GroupName']}, Group ID: {group['GroupId']}, VPC ID: {group.get('VpcId', 'N/A')}")
    except Exception as e:
        print(f"Error describing security groups: {e}")

def delete_security_group(group_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.delete_security_group(GroupId=group_id)
        print(f"Successfully deleted Security Group with ID {group_id}: {response}")
    except Exception as e:
        print(f"Error deleting Security Group with ID {group_id}: {e}")


def add_inbound_rule(group_id):
    ec2 = boto3.client('ec2')
    try:
        ip_protocol = input("Enter protocol (e.g., tcp, udp, icmp): ").strip()
        from_port = int(input("Enter starting port: "))
        to_port = int(input("Enter ending port: "))
        cidr_ip = input("Enter CIDR IP range (e.g., 0.0.0.0/0): ").strip()

        rule = {
            'IpProtocol': ip_protocol,
            'FromPort': from_port,
            'ToPort': to_port,
            'IpRanges': [{'CidrIp': cidr_ip}]
        }
        response = ec2.authorize_security_group_ingress(GroupId=group_id, IpPermissions=[rule])
        print("Added inbound rule:", response)
    except Exception as e:
        print(f"Error adding inbound rule: {e}")

def add_outbound_rule(group_id):
    ec2 = boto3.client('ec2')
    try:
        ip_protocol = input("Enter protocol (e.g., tcp, udp, icmp): ").strip()
        from_port = int(input("Enter starting port: "))
        to_port = int(input("Enter ending port: "))
        cidr_ip = input("Enter CIDR IP range (e.g., 0.0.0.0/0): ").strip()

        rule = {
            'IpProtocol': ip_protocol,
            'FromPort': from_port,
            'ToPort': to_port,
            'IpRanges': [{'CidrIp': cidr_ip}]
        }
        response = ec2.authorize_security_group_egress(GroupId=group_id, IpPermissions=[rule])
        print("Added outbound rule:", response)
    except Exception as e:
        print(f"Error adding outbound rule: {e}")

def describe_security_group_rules_with_ids(group_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_security_group_rules(Filters=[{'Name': 'group-id', 'Values': [group_id]}])
        inbound_rules = []
        outbound_rules = []

        print("\nInbound Rules:")
        for idx, rule in enumerate(response['SecurityGroupRules'], start=1):
            if not rule['IsEgress']:
                print(f"Rule {idx}: Rule ID= {rule['SecurityGroupRuleId']}, "
                      f"Protocol= {rule.get('IpProtocol', 'ALL')}, "
                      f"Ports= {rule.get('FromPort', 'ALL')}-{rule.get('ToPort', 'ALL')}, "
                      f"CIDR= {rule.get('CidrIpv4', 'N/A')}")
                inbound_rules.append(rule['SecurityGroupRuleId'])

        print("\nOutbound Rules:")
        for idx, rule in enumerate(response['SecurityGroupRules'], start=1):
            if rule['IsEgress']:
                print(f"Rule {idx}: Rule ID= {rule['SecurityGroupRuleId']}, "
                      f"Protocol= {rule.get('IpProtocol', 'ALL')}, "
                      f"Ports= {rule.get('FromPort', 'ALL')}-{rule.get('ToPort', 'ALL')}, "
                      f"CIDR= {rule.get('CidrIpv4', 'N/A')}")
                outbound_rules.append(rule['SecurityGroupRuleId'])

        return inbound_rules, outbound_rules
    except Exception as e:
        print(f"Error describing rules for Security Group {group_id}: {e}")
        return [], []

def remove_rule_inbound(group_id, rule_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.revoke_security_group_ingress(
            GroupId=group_id,
            SecurityGroupRuleIds=[rule_id]
        )
        print(f"Successfully removed inbound rule with ID {rule_id}: {response}")
    except Exception as e:
        print(f"Error removing rule with ID {rule_id}: {e}")

def remove_rule_outbound(group_id, rule_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.revoke_security_group_egress(
            GroupId=group_id,
            SecurityGroupRuleIds=[rule_id]
        )
        print(f"Successfully removed outbound rule with ID {rule_id}: {response}")
    except Exception as e:
        print(f"Error removing rule with ID {rule_id}: {e}")

def create_vpc(cidr_block):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_vpc(CidrBlock=cidr_block)
        vpc_id = response['Vpc']['VpcId']
        print(f"Created VPC: {vpc_id}")
        return response
    except Exception as e:
        print(f"Error creating VPC: {e}")

def delete_vpc(vpc_id):
    ec2 = boto3.client('ec2')
    try:
        ec2.delete_vpc(VpcId=vpc_id)
        print(f"Deleted VPC: {vpc_id}")
    except Exception as e:
        print(f"Error deleting VPC {vpc_id}: {e}")

def describe_vpcs():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_vpcs()
        for vpc in response['Vpcs']:
            vpc_id = vpc['VpcId']
            cidr_block = vpc['CidrBlock']
            state = vpc['State']
            print(f"VPC ID: {vpc_id}, CIDR Block: {cidr_block}, State: {state}")
    except Exception as e:
        print(f"Error describing VPCs: {e}")

def network_operations_menu(ec2):
    while True:
        print("\n------------------------------------------------------------")
        print("                 Amazon AWS Network Operations              ")
        print("------------------------------------------------------------")
        print("  1. Create Security Group         2. Show Security Groups  ")
        print("  3. Delete Security Group         4. Show Security Group Rules")
        print("  5. Add Outbound Rule             6. Add Inbound Rule      ")
        print("  7. Remove Outbound Rule          8. Remove Inbound Rule   ")
        print("  9. Show VPCs                    10. Create VPC            ")
        print("  11. Delete VPC                                            ")
        print("                                  99. Back to Menu          ")
        print("------------------------------------------------------------")

        try:
            number = int(input("Enter an integer: "))
        except ValueError:
            print("Invalid input!")
            continue

        if number == 99:
            break
        elif number == 1:
            group_name = input("Enter Security Group Name: ").strip()
            description = input("Enter Security Group Description: ").strip()
            vpc_id = input("Enter VPC ID: ").strip()
            if group_name and description and vpc_id:
                create_security_group(group_name, description, vpc_id)
            else:
                print("Invalid input! All fields are required.")
        elif number == 2:
            describe_security_groups()
        elif number == 3:
            group_id = input("Enter Security Group ID: ").strip()
            if group_id:
                delete_security_group(group_id)
            else:
                print("Invalid input! Security Group ID is required.")
        elif number == 4:
            group_id = input("Enter Security Group ID: ").strip()
            if group_id:
                describe_security_group_rules_with_ids(group_id)
            else:
                print("Invalid input! Security Group ID is required.")
        elif number == 5:
            group_id = input("Enter Security Group ID: ").strip()
            if group_id:
                add_outbound_rule(group_id)
            else:
                print("Invalid input! Security Group ID is required.")
        elif number == 6:
            group_id = input("Enter Security Group ID: ").strip()
            if group_id:
                add_inbound_rule(group_id)
            else:
                print("Invalid input! Security Group ID is required.")
        elif number == 7:
            group_id = input("Enter Security Group Name: ").strip()
            rule_id = input("Enter Rule ID to delete: ").strip()
            if rule_id:
                remove_rule_outbound(group_id, rule_id)
            else:
                print("Invalid input! Rule ID is required.")
        elif number == 8:
            group_id = input("Enter Security Group Name: ").strip()
            rule_id = input("Enter Rule ID to delete: ").strip()
            if rule_id:
                remove_rule_inbound(group_id, rule_id)
            else:
                print("Invalid input! Rule ID is required.")
        elif number == 9:
            describe_vpcs()
        elif number == 10:
            cidr_block = input("Enter CIDR block for the new VPC (e.g., 10.0.0.0/16): ").strip()
            if cidr_block:
                create_vpc(cidr_block)
            else:
                print("Invalid input! CIDR block is required.")
        elif number == 11:
            vpc_id = input("Enter VPC ID to delete: ").strip()
            if vpc_id:
                delete_vpc(vpc_id)
            else:
                print("Invalid input! VPC ID is required.")
        else:
            print("Invalid option!")
