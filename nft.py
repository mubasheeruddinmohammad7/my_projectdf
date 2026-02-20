import random
import time
import streamlit as st

def mint_nft(product, user_id):
    nft_id = f"DFNFT-{random.randint(1000, 9999)}"
    nft = {
        'id': nft_id,
        'name': f"{product['name']} - NFT",
        'icon': product['icon'],
        'product_id': product['id'],
        'owner': user_id,
        'minted_at': time.strftime("%Y-%m-%d %H:%M:%S"),
        'token_id': f"0x{random.getrandbits(128):032x}"
    }
    st.session_state.nfts.append(nft)
    return nft