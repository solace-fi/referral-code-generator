# Quick Start

1. Clone the repo to your local machine, and change into the new directory
```
git clone https://github.com/solace-fi/referral-code-generator.git && cd referral-code-generator
```

2. Install dependencies. Good practice to use venv: `python3 -m venv venv` => `source venv/bin/activate`
```
pip install -r requirements.txt
```

3. Create a .env file, and enter private key and RPC endpoint (example provided in .env.example)

4. In app.py, comment in/out the desired constant values for the chain ID and SolaceCoverProductV2.sol address. Default set for MATIC mainnet (lines 17-18).

5. Run script
```
python app.py
```

# Expected Output

![](https://github.com/solace-fi/referral-code-generator/blob/main/static/img/terminal_output.png)

# Explanation

The script will do the following:

1. Generate a random private key, and display it
2. Compute and display the EVM public address and referral code associated with the private key
3. Create a Solace wallet coverage policy for the script-generated EVM public address