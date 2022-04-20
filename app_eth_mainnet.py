from web3.auto import Web3
import ecdsa
from eth_keys import keys
from eth_account.messages import encode_structured_data
from eip712_structs import make_domain
from eip712_structs import EIP712Struct, Uint
from dotenv import load_dotenv
import os
import json

# Load .env file
load_dotenv()
YOUR_PRIVATE_KEY = os.getenv("YOUR_PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")

# Polygon mainnet constants
SOLACE_COVER_PRODUCT_ADDRESS = "0x501ACEbe29eabc346779BcB5Fd62Eaf6Bfb5320E"
CHAIN_ID = 1

# Create Web3 objects
w3 = Web3(Web3.HTTPProvider(RPC_URL))
abi = json.loads('[{"inputs":[{"internalType":"address","name":"governance_","type":"address"},{"internalType":"address","name":"registry_","type":"address"},{"internalType":"string","name":"asset_","type":"string"},{"internalType":"string","name":"domain_","type":"string"},{"internalType":"string","name":"version_","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"asset","type":"string"}],"name":"AssetSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"baseURI","type":"string"}],"name":"BaseURISet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"chargeCycle","type":"uint256"}],"name":"ChargeCycleSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"cooldownPeriod","type":"uint256"}],"name":"CooldownPeriodSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"policyholder","type":"address"},{"indexed":false,"internalType":"uint256","name":"startTime","type":"uint256"}],"name":"CooldownStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"policyholder","type":"address"}],"name":"CooldownStopped","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"policyholder","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"DepositMade","type":"event"},{"anonymous":false,"inputs":[],"name":"GovernanceLocked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"pendingGovernance","type":"address"}],"name":"GovernancePending","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oldGovernance","type":"address"},{"indexed":false,"internalType":"address","name":"newGovernance","type":"address"}],"name":"GovernanceTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"isReferralOn","type":"bool"}],"name":"IsReferralOnSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"maxRateDenom","type":"uint256"}],"name":"MaxRateDenomSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"maxRateNum","type":"uint256"}],"name":"MaxRateNumSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"pause","type":"bool"}],"name":"PauseSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"policyID","type":"uint256"}],"name":"PolicyCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"policyID","type":"uint256"}],"name":"PolicyDeactivated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"activeCoverLimit","type":"uint256"}],"name":"PolicyManagerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"policyID","type":"uint256"}],"name":"PolicyUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"policyholder","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"PremiumCharged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"policyholder","type":"address"},{"indexed":false,"internalType":"uint256","name":"actualPremium","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"chargedPremium","type":"uint256"}],"name":"PremiumPartiallyCharged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"referralReward","type":"uint256"}],"name":"ReferralRewardSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"rewardEarner","type":"address"},{"indexed":false,"internalType":"uint256","name":"rewardPointsEarned","type":"uint256"}],"name":"ReferralRewardsEarned","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"referralThreshold","type":"uint256"}],"name":"ReferralThresholdSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"registry","type":"address"}],"name":"RegistrySet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"policyholder","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountGifted","type":"uint256"}],"name":"RewardPointsSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"SupportedChainRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"SupportedChainSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"policyholder","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"WithdrawMade","type":"event"},{"inputs":[],"name":"acceptGovernance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder","type":"address"}],"name":"accountBalanceOf","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder_","type":"address"},{"internalType":"uint256","name":"coverLimit_","type":"uint256"},{"internalType":"uint256","name":"amount_","type":"uint256"},{"internalType":"bytes","name":"referralCode_","type":"bytes"},{"internalType":"uint256[]","name":"chains_","type":"uint256[]"}],"name":"activatePolicy","outputs":[{"internalType":"uint256","name":"policyID","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"activeCoverLimit","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"supportedChains","type":"uint256[]"}],"name":"addSupportedChains","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"asset","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"availableCoverCapacity","outputs":[{"internalType":"uint256","name":"availableCoverCapacity_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"chargeCycle","outputs":[{"internalType":"uint256","name":"chargeCycle_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"holders","type":"address[]"},{"internalType":"uint256[]","name":"premiums","type":"uint256[]"}],"name":"chargePremiums","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cooldownPeriod","outputs":[{"internalType":"uint256","name":"cooldownPeriod_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder_","type":"address"}],"name":"cooldownStart","outputs":[{"internalType":"uint256","name":"cooldownStart_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"policyID_","type":"uint256"}],"name":"coverLimitOf","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deactivatePolicy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainIndex","type":"uint256"}],"name":"getChain","outputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"policyID","type":"uint256"}],"name":"getPolicyChainInfo","outputs":[{"internalType":"uint256[]","name":"policyChains","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"referralCode","type":"bytes"}],"name":"getReferrerFromReferralCode","outputs":[{"internalType":"address","name":"referrer","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"governance","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"governanceIsLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder","type":"address"}],"name":"isReferralCodeUsed","outputs":[{"internalType":"bool","name":"isReferralCodeUsed_","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"referralCode","type":"bytes"}],"name":"isReferralCodeValid","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isReferralOn","outputs":[{"internalType":"bool","name":"isReferralOn_","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"isSupportedChain","outputs":[{"internalType":"bool","name":"status","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lockGovernance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxCover","outputs":[{"internalType":"uint256","name":"cover","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxRateDenom","outputs":[{"internalType":"uint256","name":"maxRateDenom_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxRateNum","outputs":[{"internalType":"uint256","name":"maxRateNum_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"coverLimit","type":"uint256"}],"name":"minRequiredAccountBalance","outputs":[{"internalType":"uint256","name":"minRequiredAccountBalance_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numSupportedChains","outputs":[{"internalType":"uint256","name":"count","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"status","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingGovernance","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"policyCount","outputs":[{"internalType":"uint256","name":"count","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder_","type":"address"}],"name":"policyOf","outputs":[{"internalType":"uint256","name":"policyID","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"policyID_","type":"uint256"}],"name":"policyStatus","outputs":[{"internalType":"bool","name":"status","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder_","type":"address"}],"name":"premiumsPaidOf","outputs":[{"internalType":"uint256","name":"premiumsPaid_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"referralReward","outputs":[{"internalType":"uint256","name":"referralReward_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"referralThreshold","outputs":[{"internalType":"uint256","name":"referralThreshold_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"registry","outputs":[{"internalType":"address","name":"registry_","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"removeSupportedChain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder_","type":"address"}],"name":"rewardPointsOf","outputs":[{"internalType":"uint256","name":"rewardPoints_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"riskManager","outputs":[{"internalType":"address","name":"riskManager_","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"assetName","type":"string"}],"name":"setAsset","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"baseURI_","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"chargeCycle_","type":"uint256"}],"name":"setChargeCycle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"cooldownPeriod_","type":"uint256"}],"name":"setCooldownPeriod","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"isReferralOn_","type":"bool"}],"name":"setIsReferralOn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxRateDenom_","type":"uint256"}],"name":"setMaxRateDenom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxRateNum_","type":"uint256"}],"name":"setMaxRateNum","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"paused_","type":"bool"}],"name":"setPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"pendingGovernance_","type":"address"}],"name":"setPendingGovernance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"referralReward_","type":"uint256"}],"name":"setReferralReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"referralThreshhold_","type":"uint256"}],"name":"setReferralThreshold","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"registry_","type":"address"}],"name":"setRegistry","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"policyholder_","type":"address"},{"internalType":"uint256","name":"rewardPoints_","type":"uint256"}],"name":"setRewardPoints","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"policyID","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"tokenURI_","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newCoverLimit_","type":"uint256"},{"internalType":"bytes","name":"referralCode_","type":"bytes"}],"name":"updateCoverLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"policyChains","type":"uint256[]"}],"name":"updatePolicyChainInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
contract = w3.eth.contract(address=SOLACE_COVER_PRODUCT_ADDRESS, abi=abi)

# Functions
def generate_private_key():
    # Randomly generate private key
    # ECDSA library uses os.urandom() as default source of entropy
    signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    private_key = signing_key.to_string().hex()
    print("PRIVATE KEY:", private_key)
    return private_key

def generate_public_key(private_key):
    priv_key = keys.PrivateKey(bytes.fromhex(private_key))
    pub_key = priv_key.public_key
    return pub_key.to_checksum_address()

def generate_referral_code(private_key):
    # Construct EIP712-compliant message
    domain = make_domain(
        name = "Solace.fi-SolaceCoverProduct", 
        version = "1",
        chainId = CHAIN_ID,
        verifyingContract = SOLACE_COVER_PRODUCT_ADDRESS
    )

    class SolaceReferral(EIP712Struct):
        version = Uint(256)

    message = SolaceReferral(version=1)

    # Parse EIP712-compliant message into web3.py-friendly type
    message_dict = message.to_message(domain)
    message_encoded = encode_structured_data(message_dict)

    # Sign EIP712-compliant message with private keys => Referral code
    signed_message = w3.eth.account.sign_message(message_encoded, private_key)
    referral_code = signed_message.signature.hex()
    print("REFERRAL CODE:", referral_code)

def activatePolicy(public_key):
    txn = contract.functions.activatePolicy(
        public_key, # Address of intended policyholder
        10, # Cover limit
        1, # Deposit amount
        "0x", # Empty referral code
        [137] # Array of supported chains
        ).buildTransaction({
            'chainId': CHAIN_ID,
            'gas': 500000,
            'maxFeePerGas': w3.toWei('80', 'gwei'),
            'maxPriorityFeePerGas': w3.toWei('45', 'gwei'),
            'nonce': w3.eth.get_transaction_count(generate_public_key(YOUR_PRIVATE_KEY))
        }
    )

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=YOUR_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("WAITING FOR TRANSACTION:", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("SUCCESSFUL ACTIVATEPOLICY TRANSACTION!")

def main():
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    print("PUBLIC KEY:", public_key)
    generate_referral_code(private_key)
    activatePolicy(public_key)

main()