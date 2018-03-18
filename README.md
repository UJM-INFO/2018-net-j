# 2018-net-j

# Members of the project 
 1. **MUAZ TWATY**
 2. **ABOUD ZAKARYA**
 3. **MEHDI ZARRIA**
 4. **MOHAMMED BELAIHOU**
 
# Subject description

The project consists on developing a protocol using the Block Chain logic to stock and transmit transactions between different types of users (miners or simple users) and the P2P protocol to insure the communication between the difference entities.

The Block chain protocol became more famous since the development of the crypto currency; the latter uses the block chain to stock transaction done between users and to mine new currency using a hashing algorithm. In general, the data type transmitted is text type, but it can be extended to other types such images, voice …

A Block Chain protocol uses different entities to run properly: Tracker, Members list and the chain, in the following paragraphs we will describe each entity.


# Runing the project



# Description of the architecture

Our protocol is built with the following bricks:

**The tracker**: is the entity that contains the list of connecting member on the network, by members we nominate the miners, and members having the block chain. The Tracker make a ping call for each member on the list with a period of 1 minute to check its availability on the network, in the case that a member is disconnected, he will be dropt from the list.

**The member**: In practice, the member can be a simple user, a miner or a member having the chain, for the simplicity purpose, we considered all the members as miners. A member can do send two commands to the tracker, the first one is to **ask the tracker to add him in the list of connected members, and the second one is to ask the tracker of a list of connected members to make a transaction**. 
In addition, a member do the following functionalities:
 1. **Sniff new Blocks**: The member listen in the network, if there is a new block created by a member and has been sent in the network, in that case, the member add the block to his chain. Two case can be happen, The member added a new block, or a duplicated block, for the last case, every member make a dumpChain to drop the duplicated block every 10 secondes.
 2. **Send Blocks**: A member can ask other for specific blocks, each block has an ID, if a member send to network the id\_last of the last block he has in the chain, and if another member has blocks having an ID greater that id\_last, he send theme.
 3. **Get Blocks**: When a member get the new blocks, he add theme to the stack, if they are new blocks he add theme to the chain, if not he drop theme.


In the following paragraph, we will explain how our protocol handles the transaction in a chain.

In the beginning, when a member is connected, he send the “Registration” command to the tracker. After this operation, he started sniffing the network if there is a new block created and communicated to the network, and at the same time listening if there is a request coming from the tracker to validate the presence of the member, or a request from another member asking for a blocks.

The creation of a new block, consist on using a hashing function, this function to calculate the code using the Id of the block, the data to stock, and the nonce, a validate new code must start with DIFFICULTY (default = 4) zeros. This after this, the block will be communicated to the network.

To add a block to the chain, it must be validated. The process of validation is the following.

1. **Validate the hash code**: by recalculate it, the sent hash has to be equal to the calculated one.
2. **Starting zeros**: The hash code must start with DIFFICULTY zeros.
3. **Validate the block id**: since all users have the same blocks, we have to check if the sent block is not in the already in the chain.
4. **Validate the prehash**: check the link between the last block and the new one created.
5. **Validate the balance**:  for money transfer, we check that the debited account has the necessary amount.


After the creation, the id of the new block is communicated in the network. The other members while sniffing, they get the new block, validate it and add it to the chain.

If a member is disconnected and reconnected, he inform the tracker, and ask it for a list of members in order to synchronize the block (check if there is new block created)

At this stage, we described each element of our protocol, and the interaction between those elements.
