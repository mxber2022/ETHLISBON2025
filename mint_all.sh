#!/bin/bash

KEY_FILE="minting_key.txt"
OWNER="0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
NFT_HASH="Qmbh9SQLbNRawh9Km3PMEDSxo77k1wib8fYZUdZkhPBiev"

echo "Minting required connections..."
autonomy mint --use-local connection --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/connections/abci/
autonomy mint --use-local connection --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/connections/p2p_libp2p_client/
autonomy mint --use-local connection --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/connections/ipfs/
autonomy mint --use-local connection --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/connections/ledger/

echo "Minting required protocols..."
autonomy mint --use-local protocol --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/open_aea/protocols/signing/
autonomy mint --use-local protocol --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/protocols/abci/
autonomy mint --use-local protocol --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/protocols/acn/
autonomy mint --use-local protocol --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/protocols/ipfs/
autonomy mint --use-local protocol --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/protocols/http/

echo "Minting required skills..."
autonomy mint --use-local skill --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/elia/skills/your_fsm_app_abci/
autonomy mint --use-local skill --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/skills/abstract_abci/
autonomy mint --use-local skill --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/skills/abstract_round_abci/
autonomy mint --use-local skill --key $KEY_FILE --nft $NFT_HASH --owner $OWNER ./packages/valory/skills/termination_abci/

echo "✅ All dependencies minted. You can now mint the agent."

