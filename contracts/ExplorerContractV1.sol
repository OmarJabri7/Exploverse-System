// //Contract based on [https://docs.openzeppelin.com/contracts/3.x/erc721](https://docs.openzeppelin.com/contracts/3.x/erc721)
// // SPDX-License-Identifier: MIT
// pragma solidity ^0.8.0;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
// import "@openzeppelin/contracts/utils/Counters.sol";
// import "@openzeppelin/contracts/access/Ownable.sol";
// import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

// contract Explorer is ERC721URIStorage, Ownable {
//     using Counters for Counters.Counter;
//     Counters.Counter private _tokenIds;

//     constructor(string memory _name, string memory _symbol)
//         public
//         ERC721(_name, _symbol)
//     {}

//     function mintNFT(
//         address recipient,
//         string memory tokenURI,
//         uint256 tokenId
//     ) public payable returns (uint256) {
//         _tokenIds.increment();

//         uint256 newItemId = _tokenIds.current();
//         _safeMint(recipient, tokenId);
//         _setTokenURI(tokenId, tokenURI);

//         return tokenId;
//     }
// }
