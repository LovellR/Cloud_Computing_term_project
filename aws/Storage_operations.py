import boto3

def create_volume(size, availability_zone):
    try:
        ec2 = boto3.client('ec2')
        response = ec2.create_volume(Size=size, AvailabilityZone=availability_zone, VolumeType='gp2')
        print("Created Volume:", response)
    except Exception as e:
        print(f"Error creating volume: {e}")

def attach_volume(volume_id, instance_id, device):
    try:
        ec2 = boto3.client('ec2')
        response = ec2.attach_volume(VolumeId=volume_id, InstanceId=instance_id, Device=device)
        print("Attached Volume:", response)
    except Exception as e:
        print(f"Error attaching volume: {e}")
   

def detach_volume(volume_id):
    try:
        ec2 = boto3.client('ec2')
        response = ec2.detach_volume(VolumeId=volume_id)
        print("Detached Volume:", response)
    except Exception as e:
        print(f"Error detaching volume: {e}")


def delete_volume(volume_id):
    try:
        ec2 = boto3.client('ec2')
        response = ec2.delete_volume(VolumeId=volume_id)
        print("Deleted Volume:", response)
    except Exception as e:
        print(f"Error deleting volume: {e}")

def describe_volumes():
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_volumes()
        volumes = response['Volumes']
        if not volumes:
            print("No volumes found.")
            return
        print("\nEBS Volumes:")
        for vol in volumes:
            print(f"Volume ID: {vol['VolumeId']}, Size: {vol['Size']} GiB, "
                  f"State: {vol['State']}, Attached to: {', '.join([att['InstanceId'] for att in vol.get('Attachments', [])]) or 'None'}")
    except Exception as e:
        print(f"Error describing volumes: {e}")

def storage_operations_menu(ec2):
    while True:
        print("\n------------------------------------------------------------")
        print("                     Amazon AWS Storage                     ")
        print("------------------------------------------------------------")
        print("  1. Create Volume               2. Attach Volume           ")
        print("  3. Detach Volume               4. Delete Volume           ")
        print("  5. List Volumes                                           ")
        print("                                99. Back to Menu            ")
        print("------------------------------------------------------------")

        try:
            number = int(input("Enter an integer: "))
        except ValueError:
            print("Invalid input!")
            continue

        if number == 99:
            break
        elif number == 1:
            try:
                size = int(input("Enter the volume size (in GiB): "))
                availability_zone = input("Enter the availability zone (e.g., us-east-1a): ").strip()
                if size > 0 and availability_zone:
                    create_volume(size, availability_zone)
                else:
                    print("Invalid input! Size must be > 0 and availability zone must be specified.")
            except ValueError:
                print("Invalid size input!")
        elif number == 2:
            volume_id = input("Enter the volume ID to attach: ").strip()
            instance_id = input("Enter the instance ID to attach the volume to: ").strip()
            device = input("Enter the device name (e.g., /dev/xvda): ").strip()
            if volume_id and instance_id and device:
                attach_volume(volume_id, instance_id, device)
            else:
                print("Invalid input! Volume ID, instance ID, and device name are required.")
        elif number == 3:
            volume_id = input("Enter the volume ID to detach: ").strip()
            if volume_id:
                detach_volume(volume_id)
            else:
                print("Invalid input! Volume ID is required.")
        elif number == 4:
            volume_id = input("Enter the volume ID to delete: ").strip()
            if volume_id:
                delete_volume(volume_id)
            else:
                print("Invalid input! Volume ID is required.")
        elif number == 5:
            describe_volumes()
        else:
            print("Invalid option!")
