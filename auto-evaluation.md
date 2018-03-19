# What work vs What does not work

In the following table we will list the different functionalities that our protocol should contains, and the state of each function

|Functions                |State                          |
|----------------|-------------------------------|
|Create Member|                  OK     |
|Add member to the tracker         |OK       |
|Synchronize the memeber list          |OK|
|Get the memeber list          |OK|
|Listening to network          |OK|
|Get blocks from other members          |OK|
|Create new block          |OK|
|Validate a received block         |OK|
|Add the block to the Chain          |OK|
|drop a duplicated/non valid block          |OK|
|Public/Private Key          |KO|

# Initial vs Current objectives

Our initial objective was to build a protocol assuring basic functionalities, and develop theme after. At this stage, we can say that we could run those functionalities. such as making transactions, creating blocks and ensure the communication between the different entities.

# Members organisation

**MUAZ TWATY**:

 - Synchronization of the member list in the tracker
 - Create new block
 - Validate a received block
 - Listening to the network

**ABOUD ZAKARYA**: 

 - GUI
 - Create the member
 - Development of the hashing function
 - Get blocks from other members
 - Handle the memeber commands

**MEHDI ZARRIA**: 

 - Validate a received block
 - Add the block to the chain
 - Send a new block in the network

**MOHAMMED BELAIHOU**: 

 - Add members to the tracker
 - Get member list from the tracker
 - Drop duplicated/non valid blocks


# Good Development Practices

## About documents

|Practice                |State                          |
|----------------|-------------------------------|
|Use the markdown |                  OK     |

## About git

|Practice                |State                          |
|----------------|-------------------------------|
|commit only source and configuration |OK     |
|use `.gitignore`|OK|
|do not use git just to store a zip of your project|OK|
|commit/push often|OK|
|provide good commit messages|OK|
|use English for all commit messages|OK|

## About your code
|Practice                |State                          |
|----------------|-------------------------------|
|write your code in English |OK     |
|avoid mixing spaces and tabs|OK|
|do not use git just to store a zip of your project|OK|
|keep your code clean|OK|

## Test
|Practice                |State                          |
|----------------|-------------------------------|
|test a lot and often |OK     |
|have automated tests|KO|
|have stress tests|KO|
|have tests for "bad" behaviors from other peers|OK|
|document how to use, compile, test and start your projec|OK|
|document how to understand and continue your project|OK|


