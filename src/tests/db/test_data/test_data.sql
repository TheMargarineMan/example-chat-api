INSERT INTO users (user_id, username, password) VALUES
-- Uses prehashed digests of passwords
(1, 'xX_EldenLord_Xx', '21cb88be200154e5e3ec670059387cdeab8c85829faffb2d0646bccacb2aebe07406ffca96c687cff24e3aca21ea410fa000402e268d4418a42b227da9365f65'), -- thefallenleaves
(2, 'Radagon', '4d0b3628eda2966ff4169b730f70ec33a66c900afd40fac6fd73903c0bb1fc00f76d3b8f100190e70fedd347b0863c9bf1886765a741a377c542b0b9628dfc67'), -- 2ndConsort
(3, 'Mal3n1a', '08d37e016d972d2fdb6b639d88084cc8a8ae74a8bd848df6b6c8dc9bf138dd24fa87f6319ea8f1f07458896dd64e58ea8f4b5af11935c05d6a22d4ff51ac2b59'), -- queenofrot
(4, 'Melina', 'a3a3bbec2908e1acef2d7f143de8e807f5b6d06b17186bf00569de3a1fd57fbd321b7c993d9b6a7c0cddd0870a7c73ea56ad057b1d98eae1e10417ed621474c3'), -- gloameyedqueen
(5, 'Ranni', '96a5842508595f095e4d34cbe309d715c6c521c17f61ec60f05b54900010774122ce3bc55f65453cbc19a86913b71fe52e4486eae45ccdc21d75cbde3ddc86b6'), -- ageofstars
(6, 'Brother Corhyn', '081334908e649b33e4d670e0b82ec25c9d62de4b3116acd874d31f42955780a7c2d340429101cda0a64068c1d4f707b28440da5d82d38c73a2cad6386eb0bd24'), -- GoldenOrder
(7, 'Starscourge', '946a6bd890ff80c2c9414587c7cf4851de5f3005d07a3fc2775b92aa056915f8eb887c73d9be7a47087873839f45817ffa9d3281f864060f777f473a39a9b013'), -- GRAVITAS
(8, 'GildedGraft', '1292242872c96ce78b1a7cbbb0317219d9f6cd432bb85baabd97dea7dc25a8a4f4509677cfa928968d9c81aaddae98360e7f4d626bda880dc898c0fa481557bd'), -- bearwitness
(9, 'Godfrey', 'd242e7e0ebaba0dcbd2b575145059a5727603f3917a19a0d8b1412f5fc62f33bf305b3ee3afabe97137833a4378a6b453a5f08f08daf94dfa9e6e205862b6d7f'), -- badlands4lyfe
(10, 'Morgott', 'd242e7e0ebaba0dcbd2b575145059a5727603f3917a19a0d8b1412f5fc62f33bf305b3ee3afabe97137833a4378a6b453a5f08f08daf94dfa9e6e205862b6d7f'); -- ExtinguishAmbition

ALTER SEQUENCE users_user_id_seq RESTART 11;

INSERT INTO communities (comm_id, comm_name) VALUES
(1, 'Raya Lucaria'),
(2, 'Leyendell'),
(3, 'Redmane Castle');

ALTER SEQUENCE communities_comm_id_seq RESTART 4;

INSERT INTO chats (chat_id, chat_name, comm_id) VALUES
(1, 'Grand Study Hall', 1),
(2, 'Rannis Rise', 1),
(3, 'The Foot of the Erdtree', 2),
(4, 'Erdtree Sanctuary', 2),
(5, 'Radahns Battlefield', 3),
(6, 'The Divine Tower of Caelid', 3),
(7, 'Direct Message: Morgott/Godfrey', NULL);

ALTER SEQUENCE chats_chat_id_seq RESTART 8;

INSERT INTO direct_chats (user_one, user_two, chat_id) VALUES
(9, 10, 7);

INSERT INTO messages (msg_id, message, timestamp, user_id, chat_id) VALUES
(1, 'Fools emboldened by the flame of ambition.', '2012-6-24 12:42:57', 10, 3),
(2, 'My brother in Marika you wear rags as a monarch. The Golden Order fell off.', '2012-6-24 12:43:05', 1, 3),
(3, 'Your ego is as fragile as your title of King', '2012-6-24 12:43:10', 4, 3),
(4, 'KNEEL BEFORE MORGOTT, THE OMEN KING', '2012-6-24 12:43:20', 10, 3),
(5, 'Honey, Im home from my vacation! Wait wtf.', '2012-7-24 4:20:22', 9, 3),
(6, 'Sup I run this block now', '2012-7-24 4:20:40', 1, 3),
(7, 'Nah fam cant have that', '2012-7-24 4:21:01', 9, 3),
(8, 'Now who is this bozo', '2012-7-25 10:08:04', 2, 3),
(9, 'The man who about to steal ur girl', '2012-7-25 10:08:11', 1, 3),
(10, 'Ima dip out son', '2010-7-25 10:10:10', 9, 7),
(11, 'Wait, no father please', '2010-7-25 10:10:12', 10, 7),
(12, '*disappears*', '2010-7-25 10:10:14', 9, 7);

ALTER SEQUENCE messages_msg_id_seq RESTART 13;
