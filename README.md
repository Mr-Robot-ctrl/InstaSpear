# InstaSpear

## Description
InstaSpear is a tool that demonstrates how phishing pages can be set up to mimic Instagram's login interface for educational and research purposes.

## Usage Instructions

### 1. Install Dependencies
On Kali Linux or similar, run the setup script to install all required packages:

```bash
chmod +x setup.sh
./setup.sh
```

### 2. Run the Tool
Start the main script:

```bash
python3 InstaSpear.py
```

### 3. Follow the Prompts
- Select the target device (Mobile or PC).
- Enter the desired port (default is 8080).
- Choose the hosting method:
	- Localhost only
	- Cloudflared tunnel (for public access)
	- Localhost.run tunnel (for public access)
- The tool will display a URL. Share this with your test subject (with their consent).
- Captured credentials will be saved in the corresponding `cred.log` file inside the selected site folder.

### 4. Stop the Tool
Press `CTRL+C` in the terminal to stop the server and any tunnels.

## Disclaimer

**This tool is for educational and authorized security testing purposes only.**

- Do NOT use InstaSpear to target accounts, systems, or individuals without explicit permission.
- The author is not responsible for any misuse or damage caused by this tool.
- Phishing is illegal and unethical if performed without consent. Always comply with all applicable laws and obtain proper authorization before conducting any security testing.

---
Created by Mr-Robot-ctrl
