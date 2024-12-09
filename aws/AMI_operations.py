import boto3

def create_image(instance_id, name):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_image(InstanceId=instance_id, Name=name)
        print("Created Image:", response)
    except Exception as e:
        print(f"Error creating image: {e}")

def describe_images():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_images(Owners=['self'])
        for image in response['Images']:
            print(f"Image ID: {image['ImageId']}, Name: {image['Name']}, State: {image['State']}")
    except Exception as e:
        print(f"Error describing images: {e}")

def deregister_image(image_id):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.deregister_image(ImageId=image_id)
        print(f"Deregistered Image: {image_id}")
    except Exception as e:
        print(f"Error deregistering image: {e}")

def AMI_operations_menu(ec2):
    while True:
        print("\n------------------------------------------------------------")
        print("                      AMI Operations                        ")
        print("------------------------------------------------------------")
        print("  1. Create Image                2. Describe Images         ")
        print("  3. Deregister Image                                       ")
        print("                                99. Back to Menu            ")
        print("------------------------------------------------------------")

        try:
            number = int(input("Enter an integer: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if number == 99:
            break
        elif number == 1:
            instance_id = input("Enter the instance ID to create an image: ").strip()
            name = input("Enter a name for the image: ").strip()
            if instance_id and name:
                create_image(instance_id, name)
            else:
                print("Invalid input! Both instance ID and name are required.")
        elif number == 2:
            describe_images()
        elif number == 3:
            image_id = input("Enter the image ID to deregister: ").strip()
            if image_id:
                deregister_image(image_id)
            else:
                print("Invalid input! Image ID is required.")
        else:
            print("Invalid option! Please select a valid option.")
