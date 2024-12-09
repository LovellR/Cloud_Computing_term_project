import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def init():
    try:
        session = boto3.Session(profile_name='default')
        ec2 = session.client('ec2', region_name='us-east-1')
        return ec2
    except NoCredentialsError:
        print("AWS 자격 증명을 찾을 수 없습니다.")
        exit()
    except PartialCredentialsError:
        print("AWS 자격 증명이 불완전합니다.")
        exit()

def list_instances(ec2):
    print("Listing instances....")
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"[id] {instance['InstanceId']}, "
                      f"[AMI] {instance['ImageId']}, "
                      f"[type] {instance['InstanceType']}, "
                      f"[state] {instance['State']['Name']}, "
                      f"[monitoring state] {instance.get('Monitoring', {}).get('State', 'unknown')}")
    except Exception as e:
        print(f"Error: {str(e)}")

def available_zones(ec2):
    print("Available zones....")
    try:
        response = ec2.describe_availability_zones()
        for zone in response['AvailabilityZones']:
            print(f"[id] {zone['ZoneId']}, [region] {zone['RegionName']}, [zone] {zone['ZoneName']}")
        print(f"You have access to {len(response['AvailabilityZones'])} Availability Zones.")
    except Exception as e:
        print(f"Error: {str(e)}")

def start_instance(ec2, instance_id):
    print(f"Starting instance {instance_id}...")
    try:
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Successfully started instance {instance_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def available_regions(ec2):
    print("Available regions....")
    try:
        regions = ec2.describe_regions()
        for region in regions['Regions']:
            print(f"[region] {region['RegionName']}, [endpoint] {region['Endpoint']}")
    except Exception as e:
        print(f"Error: {str(e)}")

def stop_instance(ec2, instance_id):
    print(f"Stopping instance {instance_id}...")
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Successfully stopped instance {instance_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def create_instance(ec2, ami_id):
    print(f"Creating instance with AMI {ami_id}...")
    try:
        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Successfully created instance {instance_id} with AMI {ami_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def reboot_instance(ec2, instance_id):
    print(f"Rebooting instance {instance_id}...")
    try:
        ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"Successfully rebooted instance {instance_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def list_images(ec2):
    print("Listing images....")
    try:
        response = ec2.describe_images(Owners=['self'])
        for image in response['Images']:
            print(f"[ImageID] {image['ImageId']}, [Name] {image['Name']}, [Owner] {image['OwnerId']}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    ec2 = init()
    while True:
        print("\n------------------------------------------------------------")
        print("           Amazon AWS Control Panel using boto3             ")
        print("------------------------------------------------------------")
        print("  1. list instance                2. available zones        ")
        print("  3. start instance               4. available regions      ")
        print("  5. stop instance                6. create instance        ")
        print("  7. reboot instance              8. list images            ")
        print("                                 99. quit                   ")
        print("------------------------------------------------------------")

        try:
            number = int(input("Enter an integer: "))
        except ValueError:
            print("Invalid input!")
            continue

        if number == 99:
            print("bye!")
            break

        if number == 1:
            list_instances(ec2)
        elif number == 2:
            available_zones(ec2)
        elif number == 3:
            instance_id = input("Enter instance id: ").strip()
            if instance_id:
                start_instance(ec2, instance_id)
        elif number == 4:
            available_regions(ec2)
        elif number == 5:
            instance_id = input("Enter instance id: ").strip()
            if instance_id:
                stop_instance(ec2, instance_id)
        elif number == 6:
            ami_id = input("Enter AMI id: ").strip()
            if ami_id:
                create_instance(ec2, ami_id)
        elif number == 7:
            instance_id = input("Enter instance id: ").strip()
            if instance_id:
                reboot_instance(ec2, instance_id)
        elif number == 8:
            list_images(ec2)
        else:
            print("Invalid option!")