# BlockChain Protocol

## Register
#### request
```
REGISTER
IP:PORT
```
#### response
`OK`
#### description
*direction:* member --> tracker
*occurrence:* The first time the member register to the network and every time the member come back online.


## Get Members
#### request
`GETMEMBERS`
#### response
```
IP:PORT
IP:PORT
IP:PORT
...
END
```
#### description
maximum 10 members
*direction:* member --> tracker
*occurrence:* before exchanging blocks


## Ping
#### request
`PING`
#### response
`OK`
#### description
*direction:* tracker --> member (from list)
*Case:* time out remove member and update tracker's list of online members
*occurrence:* periodically


## Send block 
#### request 
`SENDBLOCK`
`BLOCKDUMP`
#### response
`OK`
*case:* invalid block
`INVALID`
*case:* dropped block (reciever's chain is short)
`DROP`
#### description 
*direction :* member <--> member
*occurrence:* after a valid block is added by a member
*process:* validation of block, broadcast if valid to other available members 


## Get block
#### request
`GETBLOCK`
`ID`
#### response
`BLOCKDUMP`
*case:* not found
`NONE`
#### description
*direction:* member <--> member
*occurrence:* periodically ask the network for the increment block to complete the chain
