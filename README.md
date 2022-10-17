# Domain Management System (not)
WIP: shit can and will break     
# How to use:
1. Install python3 (duh)
2. Install the requirements: `pip3 install -r requirements.txt`
3. Run init.py to download maxmind db `python3 init.py`
4. Edit `main.py`, change `zoneid`, `domain`, `X-Auth-Email` and `X-Auth-Key` to your own
5. Use screen or systemctl or whatever the fuck to make sure that this shit doesn't blow up.

# Defaults
- listens on port 105 on 0.0.0.0, you can change in `main.py`
- yes i know im using fucking flask gimme a break
- if shit blows up open issues or pr