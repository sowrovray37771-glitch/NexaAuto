import time
import random
import requests
from playwright.sync_api import sync_playwright

# ৫০টি আমেরিকান Unisex First Name ও Surname
FIRST_NAMES = [
    "Avery", "Riley", "Jordan", "Parker", "Taylor", "Cameron", "Quinn", "Finley", "Reese", "Rowan",
    "Hayden", "Emerson", "Charlie", "Dakota", "Peyton", "Skyler", "Morgan", "Amari", "River", "Phoenix",
    "Tatum", "Sawyer", "Sage", "Rory", "Logan", "Hunter", "Carter", "Dylan", "Jayden", "Ezra",
    "Micah", "Eden", "Remy", "Elliott", "Dallas", "Kendall", "Harlow", "Milan", "Shiloh", "Sutton",
    "Armani", "Lennon", "Reign", "Frankie", "Oakley", "Robin", "Casey", "Jessie", "Skylar", "Jamie"
]

SURNAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts"
]

def get_proxy_dict(proxy_str):
    if not proxy_str.strip():
        return None, None
    parts = proxy_str.split(':')
    if len(parts) == 4:
        req_proxy = f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
        pw_proxy = {"server": f"http://{parts[0]}:{parts[1]}", "username": parts[2], "password": parts[3]}
        return {"http": req_proxy, "https": req_proxy}, pw_proxy
    elif len(parts) == 2:
        req_proxy = f"http://{parts[0]}:{parts[1]}"
        pw_proxy = {"server": f"http://{parts[0]}:{parts[1]}"}
        return {"http": req_proxy, "https": req_proxy}, pw_proxy
    else:
        print("Invalid proxy format.")
        return None, None

def test_proxy(req_proxy, link2):
    try:
        ip_info = requests.get("http://ip-api.com/json", proxies=req_proxy, timeout=10).json()
        print(f"Proxy Info -> IP: {ip_info.get('query')}, Country: {ip_info.get('country')}, City: {ip_info.get('city')}")
        
        start_time = time.time()
        requests.get(link2, proxies=req_proxy, timeout=10)
        return (time.time() - start_time) * 1000
    except Exception:
        return 99999 

def main():
    print("=== Setup System ===")
    
    target_sets = int(input("How many Sets do you want to run?: "))
    
    phone_numbers = []
    print("Enter phone numbers (Double enter to stop):")
    while True:
        num = input()
        if num == "":
            break
        phone_numbers.append(num)
        
    password = input("Enter Password: ")
    link1 = input("Enter 1st Link: ")
    link2 = input("Enter 2nd Link: ")

    # Proxy Testing Loop (Optional / Skippable)
    pw_proxy_config = None
    while True:
        proxy_str = input("Enter Proxy (host:port:user:pass) or press Enter to skip: ")
        
        if proxy_str == "":
            print("⚠️ No proxy entered. Running without proxy (Normal Connection).")
            break
            
        req_proxy, pw_proxy_config = get_proxy_dict(proxy_str)
        if not req_proxy:
            continue
            
        success = False
        for i in range(1, 7):
            print(f"Testing proxy... Attempt {i}/6")
            latency = test_proxy(req_proxy, link2)
            print(f"Latency: {latency:.2f} ms")
            
            if latency < 6000:
                print("✅ Proxy connected successfully!")
                success = True
                break
            else:
                print("❌ Latency over 6000ms.")
                time.sleep(1)
                
        if success:
            break
        else:
            print("Failed 6 times. Please provide a new proxy or press Enter to skip.")

    # Playwright Automation Start (Sequential Execution)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        user_agent_1 = "Mozilla/5.0 (Linux; Android 16; motorola edge 50 fusion Build/W1UUIS36H.110-42-4) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/157.0.8103.31 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/586.0.0.1.53;IABMV/1;]"
        user_agent_2 = "Mozilla/5.0 (Linux; Android 9; SM-A205YN Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 [FBAN/DiscoverApp;FBAV/2.0.0.0.1266;]"
        
        try:
            # --- PROFILE 1 (MASTER NUMBER CHECKER) ---
            print("\n[Master Profile] Opening Global Profile 1 (No Proxy)...")
            context1 = browser.new_context(
                user_agent=user_agent_1,
                viewport={"width": 360, "height": 550},
                is_mobile=True,
                has_touch=True
            )
            page1 = context1.new_page()
            page1.set_default_timeout(60000)
            
            number_index = 0
            
            for set_idx in range(1, target_sets + 1):
                print(f"\n========================================")
                print(f"📌 Starting Set {set_idx} of {target_sets}")
                print(f"========================================")
                
                successful_number = None
                
                # Profile 1 searches for a valid number
                while number_index < len(phone_numbers):
                    number = phone_numbers[number_index]
                    number_index += 1
                    
                    print(f"[Set {set_idx}] Profile 1 testing number: {number}")
                    page1.goto(link2)
                    page1.get_by_role("textbox").first.fill(number)
                    page1.get_by_role("button", name="Search").click()
                    
                    try:
                        page1.wait_for_selector("text=Create new account", timeout=5000)
                        print(f"[Set {set_idx}] ✅ Found 'Create new account' for number: {number}")
                        successful_number = number
                        break
                    except:
                        print(f"[Set {set_idx}] ❌ 'Create new account' not found for {number}. Trying next...")
                        continue
                
                if not successful_number:
                    print(f"\n[Set {set_idx}] ❌ No more valid numbers available in the list. Stopping.")
                    break
                
                # ==========================================
                # PROFILE 2 (REGISTRATION) FOR THIS SET
                # ==========================================
                print(f"\n[Set {set_idx}] Opening Profile 2 for number: {successful_number}")
                context2 = browser.new_context(
                    user_agent=user_agent_2,
                    viewport={"width": 360, "height": 550},
                    is_mobile=True,
                    has_touch=True
                )
                page2 = context2.new_page()
                page2.set_default_timeout(60000)
                
                page2.goto(link1)
                page2.get_by_role("button", name="Get Started").click()
                page2.wait_for_load_state("load")
                
                f_name = random.choice(FIRST_NAMES)
                l_name = random.choice(SURNAMES)
                print(f"[Set {set_idx}] Filling Name: {f_name} {l_name}")
                page2.get_by_label("First name", exact=False).fill(f_name)
                page2.get_by_label("Surname", exact=False).fill(l_name)
                page2.get_by_role("button", name="Next").click()
                page2.wait_for_load_state("load")
                
                year = random.randint(1980, 2002)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                dob = f"{year}-{month:02d}-{day:02d}"
                print(f"[Set {set_idx}] Filling DOB: {dob}")
                page2.locator("input[type='date']").fill(dob)
                page2.get_by_role("button", name="Next").click()
                page2.wait_for_load_state("load")

                gender = random.choice(["Female", "Male"])
                print(f"[Set {set_idx}] Selecting Gender: {gender}")
                page2.get_by_role("radio", name=gender, exact=True).click()
                page2.get_by_role("button", name="Next").click()
                page2.wait_for_load_state("load")

                print(f"[Set {set_idx}] Filling Mobile Number: {successful_number}")
                page2.get_by_role("textbox", name="Mobile number", exact=False).fill(successful_number)
                page2.get_by_role("button", name="Next").click()
                page2.wait_for_load_state("load")

                print(f"[Set {set_idx}] Filling Password...")
                page2.locator("input[type='password']").fill(password)
                page2.get_by_role("button", name="Next").click()
                page2.wait_for_load_state("load")

                print(f"[Set {set_idx}] Clicking 'Save' for login info...")
                page2.get_by_role("button", name="Save").click()
                page2.wait_for_load_state("load")

                print(f"[Set {set_idx}] Clicking 'I agree'...")
                page2.get_by_role("button", name="I agree").click()
                page2.wait_for_load_state("load")

                print(f"[Set {set_idx}] Selecting 'Send code via SMS'...")
                page2.get_by_role("radio", name="Send code via SMS", exact=False).click()
                page2.get_by_role("button", name="Continue").click()
                page2.wait_for_load_state("load")
                
                print(f"[Set {set_idx}] ✅ Profile 2 completed.")

                # ==========================================
                # PROFILE 3 (VERIFICATION) FOR THIS SET
                # ==========================================
                print(f"\n[Set {set_idx}] Opening Profile 3...")
                context_kwargs = {
                    "user_agent": user_agent_1,
                    "viewport": {"width": 360, "height": 550},
                    "is_mobile": True,
                    "has_touch": True
                }
                if pw_proxy_config:
                    context_kwargs["proxy"] = pw_proxy_config
                    print(f"[Set {set_idx}] Using Proxy for Profile 3.")
                else:
                    print(f"[Set {set_idx}] Running without proxy (Normal Connection).")

                context3 = browser.new_context(**context_kwargs)
                page3 = context3.new_page()
                page3.set_default_timeout(60000)
                
                page3.goto(link2)

                print(f"[Set {set_idx}] Searching number: {successful_number}")
                page3.get_by_role("textbox").first.fill(successful_number)
                page3.get_by_role("button", name="Search").click()
                page3.wait_for_load_state("load")

                print(f"[Set {set_idx}] Clicking 'Try another way' (Password page)...")
                page3.get_by_role("button", name="Try another way").click()
                page3.wait_for_load_state("load")

                print(f"[Set {set_idx}] Selecting 'Send code via SMS' (1st time)...")
                page3.get_by_role("radio", name="Send code via SMS", exact=False).click()
                page3.get_by_role("button", name="Continue").click()
                page3.wait_for_load_state("load")

                print(f"[Set {set_idx}] Clicking 'Try another way' (6-digit code page)...")
                page3.get_by_role("button", name="Try another way").click()
                page3.wait_for_load_state("load")

                print(f"[Set {set_idx}] Selecting 'Send code via SMS' (2nd time)...")
                page3.get_by_role("radio", name="Send code via SMS", exact=False).click()
                page3.get_by_role("button", name="Continue").click()
                page3.wait_for_load_state("load")

                print(f"[Set {set_idx}] 🎉 Set {set_idx} completed successfully!")

            print("\n========================================")
            print("✅ All requested Sets have finished processing!")
            print("⚠️ All browser windows will remain OPEN and ACTIVE indefinitely.")
            print("🛑 Press Ctrl+C in this terminal to stop and close everything.")
            print("========================================")
            
            # Keep alive loop
            while True:
                time.sleep(10)

        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            print("⚠️ Script paused due to error, but all opened profiles will remain open.")
            print("🛑 Press Ctrl+C in this terminal to stop.")
            
            while True:
                time.sleep(10)

if __name__ == "__main__":
    main()
