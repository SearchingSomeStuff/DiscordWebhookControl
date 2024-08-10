from dhooks import Webhook, Embed
import requests
import threading
import time

def test_webhook(webhook_url):
    try:
        response = requests.get(webhook_url)
        if response.status_code == 200:
            print("Webhook is valid.")
            return True
        else:
            print(f"Invalid webhook: Received status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Invalid webhook: {e}")
        return False


def rename_webhook(webhook):
    name = input("Enter new webhook name: ")
    try:
        webhook.modify(name=name)
        print(f"Webhook renamed to: {name}")
    except Exception as e:
        print(f"Failed to rename webhook: {e}")


def send_message(webhook):
    message = input("Enter the message to send: ")
    try:
        webhook.send(message)
        print("Message sent.")
    except Exception as e:
        print(f"Failed to send message: {e}")


def spam_messages(webhook):
    message = input("Enter the message to spam: ")
    delay = float(input("Enter delay between messages (seconds): "))
    spam_count = int(input("Enter the number of messages to spam: "))

    def spam():
        for _ in range(spam_count):
            try:
                webhook.send(message)
                print("Spammed message sent.")
                time.sleep(delay)
            except Exception as e:
                print(f"Failed to spam message: {e}")
                break

    # Run the spamming function in a separate thread to prevent blocking
    threading.Thread(target=spam).start()


def delete_webhook(webhook):
    confirmation = input("Are you sure you want to delete this webhook? (y/n): ")
    if confirmation.lower() == 'y':
        try:
            webhook.delete()
            print("Webhook deleted.")
            # Check if webhook is deleted
            response = requests.get(webhook.url)
            if response.status_code == 404:
                print("Webhook successfully deleted.")
                return True
            else:
                print("Webhook deletion failed.")
        except Exception as e:
            print(f"Failed to delete webhook: {e}")
    else:
        print("Webhook deletion canceled.")
    return False


def logout():
    print("Logging out...")
    return input("Enter new webhook URL: ")


def send_embed(webhook):
    description = input("Enter the description of the embed: ")
    color_input = input("Enter the color of the embed (in hex, e.g., '0x5CDBF0') [Press Enter for default white]: ")
    try:
        color = int(color_input, 16) if color_input else 0xFFFFFF  # Default to white if no input
    except ValueError:
        print("Invalid color input. Using default color.")
        color = 0xFFFFFF  # Default to white if input is invalid

    embed = Embed(description=description, color=color, timestamp='now')

    author_name = input("Enter the author's name (optional): ")
    author_icon = input("Enter the author's icon URL (optional): ")
    if author_name:
        embed.set_author(name=author_name, icon_url=author_icon if author_icon else None)

    while True:
        field_name = input("Enter the field name (leave blank to stop adding fields): ")
        if not field_name:
            break
        field_value = input("Enter the field value: ")
        embed.add_field(name=field_name, value=field_value)

    footer_text = input("Enter the footer text (optional): ")
    footer_icon = input("Enter the footer icon URL (optional): ")
    if footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_icon if footer_icon else None)

    thumbnail = input("Enter the thumbnail URL (optional): ")
    if thumbnail:
        embed.set_thumbnail(thumbnail)

    image = input("Enter the image URL (optional): ")
    if image:
        embed.set_image(image)

    try:
        webhook.send(embed=embed)
        print("Embed sent.")
    except Exception as e:
        print(f"Failed to send embed: {e}")


def main():
    webhook_url = input("Enter webhook URL: ")

    while not test_webhook(webhook_url):
        print("Please enter a valid webhook URL.")
        webhook_url = input("Enter webhook URL: ")

    webhook = Webhook(webhook_url)

    while True:
        print("\n--- Webhook Control Panel ---")
        print("[1] Rename webhook")
        print("[2] Send message")
        print("[3] Spam messages")
        print("[4] Delete Webhook")
        print("[5] Logout")
        print("[6] Send Embed")
        print("[0] Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            rename_webhook(webhook)
        elif choice == '2':
            send_message(webhook)
        elif choice == '3':
            spam_messages(webhook)
        elif choice == '4':
            if delete_webhook(webhook):
                webhook_url = input("Enter new webhook URL: ")
                while not test_webhook(webhook_url):
                    print("Please enter a valid webhook URL.")
                    webhook_url = input("Enter webhook URL: ")
                webhook = Webhook(webhook_url)
        elif choice == '5':
            webhook_url = logout()
            while not test_webhook(webhook_url):
                print("Please enter a valid webhook URL.")
                webhook_url = input("Enter webhook URL: ")
            webhook = Webhook(webhook_url)
        elif choice == '6':
            send_embed(webhook)
        elif choice == '0':
            print("Exiting...")
            exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
