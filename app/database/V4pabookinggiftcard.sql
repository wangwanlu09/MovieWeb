-- run after V4padatabase.sql, python populate_tables.py

USE `group4lincoln$moviemagic`;

INSERT INTO bookings (bookingid, booking_date, booking_time, no_of_tickets, total_amount, giftcardid, giftcard_deducted, payment_amount, customerid, sessionid)
VALUES
(1, '2024-01-16', '13:39:36', 3, 48, NULL, 0, 48, 2, 364),
(2, '2024-01-16', '13:49:17', 5, 92, NULL, 0, 92, 1, 375),
(3, '2024-01-16', '13:52:48', 3, 48, NULL, 0, 48, 131, 363),
(4, '2024-01-28', '11:01:07', 3, 58, NULL, 0, 58, 1, 382),
(5, '2024-01-28', '11:04:26', 4, 66, NULL, 0, 66, 4, 382),
(6, '2024-01-28', '11:08:20', 5, 80, NULL, 0, 80, 5, 382),
(7, '2024-01-28', '11:11:03', 2, 36, NULL, 0, 36, 6, 382),
(8, '2024-01-28', '19:23:12', 4, 76, NULL, 0, 76, 7, 324),
(11, '2024-01-29', '14:07:43', 3, 56, NULL, 0, 56, 2, 292),
(12, '2024-01-29', '14:33:38', 2, 34, NULL, 0, 34, 13, 292),
(13, '2024-01-29', '14:37:45', 2, 36, NULL, 0, 36, 20, 292),
(15, '2024-01-29', '14:45:17', 1, 20, NULL, 0, 20, 138, 292),
(16, '2024-02-03', '20:47:11', 8, 130, NULL, 0, 130, 21, 221),
(17, '2024-02-03', '20:52:14', 5, 80, NULL, 0, 80, 144, 221),
(18, '2024-02-03', '20:55:28', 15, 250, NULL, 0, 250, 27, 221),
(19, '2024-02-03', '21:00:42', 5, 80, NULL, 0, 80, 37, 221),
(20, '2024-02-04', '20:54:02', 10, 180, NULL, 0, 180, 8, 388),
(21, '2024-02-04', '20:58:00', 7, 128, NULL, 0, 128, 11, 388),
(22, '2024-02-04', '21:04:39', 5, 50, NULL, 0, 50, 13, 401),
(23, '2024-02-04', '21:07:55', 5, 50, NULL, 0, 50, 13, 403),
(24, '2024-02-04', '21:12:24', 8, 132, NULL, 0, 132, 2, 228),
(25, '2024-02-04', '21:20:58', 4, 72, NULL, 0, 72, 22, 400),
(26, '2024-02-04', '21:25:46', 10, 180, NULL, 0, 180, 15, 400),
(27, '2024-02-05', '07:33:46', 7, 136, NULL, 0, 136, 10, 400),
(28, '2024-02-05', '07:37:28', 6, 108, NULL, 0, 108, 17, 400),
(29, '2024-02-05', '07:41:10', 6, 108, NULL, 0, 108, 17, 414),
(30, '2024-02-05', '07:44:27', 5, 100, NULL, 0, 100, 16, 400),
(33, '2024-02-05', '07:58:44', 5, 80, NULL, 0, 80, 17, 400),
(34, '2024-02-05', '08:01:45', 4, 76, NULL, 0, 76, 20, 400),
(35, '2024-02-05', '08:04:53', 5, 100, NULL, 0, 100, 21, 400),
(36, '2024-02-05', '13:31:36', 6, 108, NULL, 0, 108, 25, 400),
(37, '2024-02-05', '13:35:15', 2, 40, NULL, 0, 40, 25, 234),
(40, '2024-02-05', '13:52:56', 4, 60, NULL, 0, 60, 39, 234),
(41, '2024-02-05', '13:58:56', 2, 40, NULL, 0, 40, 40, 400),
(42, '2024-02-05', '14:01:37', 5, 50, NULL, 0, 50, 44, 230),
(43, '2024-02-05', '14:07:09', 3, 30, NULL, 0, 30, 45, 230),
(44, '2024-02-05', '14:11:43', 5, 100, NULL, 0, 100, 48, 400),
(45, '2024-02-05', '14:17:17', 3, 30, NULL, 0, 30, 55, 230),
(46, '2024-02-06', '11:38:33', 2, 20, NULL, 0, 20, 46, 231),
(47, '2024-02-06', '11:43:40', 5, 50, NULL, 0, 50, 51, 231),
(48, '2024-02-06', '11:48:25', 1, 10, NULL, 0, 10, 53, 231),
(49, '2024-02-06', '11:50:53', 1, 10, NULL, 0, 10, 56, 231),
(50, '2024-02-06', '11:54:52', 1, 10, NULL, 0, 10, 60, 231),
(51, '2024-02-06', '12:17:00', 2, 40, NULL, 0, 40, 83, 413),
(52, '2024-02-06', '12:22:20', 2, 36, NULL, 0, 36, 85, 413),
(53, '2024-02-06', '12:24:53', 1, 16, NULL, 0, 16, 97, 413),
(54, '2024-02-06', '12:27:44', 1, 16, NULL, 0, 16, 98, 413),
(55, '2024-02-06', '12:29:53', 1, 20, NULL, 0, 20, 99, 413),
(56, '2024-02-06', '12:44:44', 1, 20, NULL, 0, 20, 112, 413),
(57, '2024-02-06', '12:47:11', 1, 16, NULL, 0, 16, 113, 413),
(58, '2024-02-06', '12:52:39', 1, 20, NULL, 0, 20, 14, 413),
(59, '2024-02-06', '12:55:01', 1, 18, NULL, 0, 18, 20, 413),
(60, '2024-02-06', '12:57:33', 2, 36, NULL, 0, 36, 11, 413),
(62, '2024-02-06', '13:16:23', 1, 20, NULL, 0, 20, 42, 236),
(63, '2024-02-06', '13:18:28', 1, 20, NULL, 0, 20, 41, 233),
(64, '2024-02-06', '13:21:44', 2, 32, NULL, 0, 32, 21, 233), 
(65, '2024-02-06', '13:24:18', 2, 30, NULL, 0, 30, 31, 233),
(66, '2024-02-09', '12:40:19', 2, 32, NULL, 0, 32, 63, 243),
(67, '2024-02-09', '12:43:14', 2, 32, NULL, 0, 32, 65, 243),
(68, '2024-02-09', '12:46:43', 2, 40, NULL, 0, 40, 75, 242),
(69, '2024-02-09', '12:54:55', 2, 36, NULL, 0, 36, 66, 242),
(70, '2024-02-09', '12:58:47', 3, 48, NULL, 0, 48, 83, 242),
(71, '2024-02-09', '13:03:35', 2, 40, NULL, 0, 40, 68, 427),
(72, '2024-02-09', '13:06:00', 4, 64, NULL, 0, 64, 77, 175),
(73, '2024-02-09', '13:10:01', 2, 32, NULL, 0, 32, 25, 171),
(74, '2024-02-09', '13:12:30', 2, 40, NULL, 0, 40, 38, 171),
(75, '2024-02-09', '13:18:12', 2, 32, NULL, 0, 32, 44, 171),
(77, '2024-02-09', '14:54:03', 2, 40, NULL, 0, 40, 25, 171),
(78, '2024-02-09', '14:58:19', 2, 20, NULL, 0, 20, 32, 454),
(79, '2024-02-11', '20:59:15', 3, 60, NULL, 0, 60, 1, 448),
(80, '2024-02-11', '21:02:23', 2, 40, NULL, 0, 40, 76, 447),
(81, '2024-02-11', '21:30:55', 5, 100, NULL, 0, 100, 83, 272),
(82, '2024-02-11', '21:34:17', 5, 80, NULL, 0, 80, 86, 272),
(83, '2024-02-11', '21:38:42', 10, 170, NULL, 0, 170, 92, 272),
(84, '2024-02-11', '21:41:13', 5, 70, NULL, 0, 70, 105, 272),
(85, '2024-02-11', '21:44:47', 5, 100, NULL, 0, 100, 111, 272),
(86, '2024-02-11', '21:47:23', 5, 70, NULL, 0, 70, 115, 272),
(87, '2024-02-11', '21:59:06', 5, 100, NULL, 0, 100, 95, 272),
(88, '2024-02-11', '22:01:48', 4, 64, NULL, 0, 64, 70, 272)
;

INSERT INTO booking_seats (bsid, bookingid, seatid, is_checkin)
VALUES
(1, 1, 6, 1),
(2, 1, 7, 1),
(3, 1, 8, 1),
(4, 2, 49, 1),
(5, 2, 50, 1),
(6, 2, 51, 1),
(7, 2, 52, 1),
(8, 2, 53, 1),
(9, 3, 3, 1),
(10, 3, 15, 1),
(11, 3, 16, 1),
(12, 4, 49, 1),
(13, 4, 50, 1),
(14, 4, 51, 1),
(15, 5, 87, 1),
(16, 5, 88, 1),
(17, 5, 90, 1),
(18, 5, 91, 1),
(19, 6, 77, 1),
(20, 6, 78, 1),
(21, 6, 79, 1),
(22, 6, 81, 1),
(23, 6, 82, 1),
(24, 7, 95, 1),
(25, 7, 96, 1),
(26, 8, 37, 1),
(27, 8, 38, 1),
(28, 8, 39, 1),
(29, 8, 40, 1),
(34, 11, 39, 1),
(35, 11, 40, 1),
(36, 11, 41, 1),
(37, 12, 45, 1),
(38, 12, 46, 1),
(39, 13, 31, 1),
(40, 13, 32, 1),
(43, 15, 43, 1),
(44, 16, 87, 1),
(45, 16, 88, 1),
(46, 16, 89, 1),
(47, 16, 90, 1),
(48, 16, 91, 1),
(49, 16, 92, 1),
(50, 16, 93, 1),
(51, 16, 94, 1),
(52, 17, 73, 1),
(53, 17, 74, 1),
(54, 17, 77, 1),
(55, 17, 78, 1),
(56, 17, 79, 1),
(57, 18, 67, 1),
(58, 18, 68, 1),
(59, 18, 69, 1),
(60, 18, 70, 1),
(61, 18, 75, 1),
(62, 18, 76, 1),
(63, 18, 80, 1),
(64, 18, 81, 1),
(65, 18, 82, 1),
(66, 18, 83, 1),
(67, 18, 84, 1),
(68, 18, 85, 1),
(69, 18, 86, 1),
(70, 18, 95, 1),
(71, 18, 96, 1),
(72, 19, 61, 1),
(73, 19, 62, 1),
(74, 19, 63, 1),
(75, 19, 64, 1),
(76, 19, 65, 1),
(77, 20, 126, 1),
(78, 20, 127, 1),
(79, 20, 128, 1),
(80, 20, 129, 1),
(81, 20, 130, 1),
(82, 20, 135, 1),
(83, 20, 136, 1),
(84, 20, 137, 1),
(85, 20, 138, 1),
(86, 20, 139, 1),
(87, 21, 123, 1),
(88, 21, 124, 1),
(89, 21, 140, 1),
(90, 21, 141, 1),
(91, 21, 142, 1),
(92, 21, 143, 1),
(93, 21, 144, 1),
(94, 22, 135, 1),
(95, 22, 136, 1),
(96, 22, 137, 1),
(97, 22, 138, 1),
(98, 22, 139, 1),
(99, 23, 136, 1),
(100, 23, 137, 1),
(101, 23, 138, 1),
(102, 23, 139, 1),
(103, 23, 140, 1),
(104, 24, 87, 1),
(105, 24, 88, 1),
(106, 24, 89, 1),
(107, 24, 90, 1),
(108, 24, 91, 1),
(109, 24, 92, 1),
(110, 24, 93, 1),
(111, 24, 94, 1),
(112, 25, 382, 1),
(113, 25, 383, 1),
(114, 25, 385, 1),
(115, 25, 394, 1),
(116, 26, 373, 1),
(117, 26, 375, 1),
(118, 26, 384, 1),
(119, 26, 376, 1),
(120, 26, 377, 1),
(121, 26, 397, 1),
(122, 26, 398, 1),
(123, 26, 399, 1),
(124, 26, 400, 1),
(125, 26, 401, 1),
(126, 27, 368, 1),
(127, 27, 369, 1),
(128, 27, 370, 1),
(129, 27, 371, 1),
(130, 27, 372, 1),
(131, 27, 378, 1),
(132, 27, 379, 1),
(133, 28, 387, 1),
(134, 28, 388, 1),
(135, 28, 389, 1),
(136, 28, 395, 1),
(137, 28, 404, 1),
(138, 28, 396, 1),
(139, 29, 395, 1),
(140, 29, 404, 1),
(141, 29, 396, 1),
(142, 29, 397, 1),
(143, 29, 398, 1),
(144, 29, 399, 1),
(145, 30, 358, 1),
(146, 30, 359, 1),
(147, 30, 360, 1),
(148, 30, 361, 1),
(149, 30, 362, 1),
(158, 33, 347, 1),
(159, 33, 348, 1),
(160, 33, 349, 1),
(161, 33, 350, 1),
(162, 33, 351, 1),
(163, 34, 340, 1),
(164, 34, 341, 1),
(165, 34, 342, 1),
(166, 34, 343, 1),
(167, 35, 335, 1),
(168, 35, 344, 1),
(169, 35, 336, 1),
(170, 35, 337, 1),
(171, 35, 338, 1),
(172, 36, 322, 1),
(173, 36, 323, 1),
(174, 36, 325, 1),
(175, 36, 334, 1),
(176, 36, 326, 1),
(177, 36, 327, 1),
(178, 37, 87, 1),
(179, 37, 88, 1),
(189, 40, 80, 1),
(190, 40, 81, 1),
(191, 40, 83, 1),
(192, 40, 84, 1),
(193, 41, 298, 1),
(194, 41, 299, 1),
(195, 42, 87, 1),
(196, 42, 88, 1),
(197, 42, 89, 1),
(198, 42, 90, 1),
(199, 42, 91, 1),
(200, 43, 92, 1),
(201, 43, 93, 1),
(202, 43, 94, 1),
(203, 44, 411, 1),
(204, 44, 412, 1),
(205, 44, 413, 1),
(206, 44, 415, 1),
(207, 44, 424, 1),
(208, 45, 77, 1),
(209, 45, 78, 1),
(210, 45, 79, 1),
(211, 46, 90, 1),
(212, 46, 91, 1),
(213, 47, 87, 1),
(214, 47, 88, 1),
(215, 47, 89, 1),
(216, 47, 92, 1),
(217, 47, 93, 1),
(218, 48, 94, 1),
(219, 49, 78, 1),
(220, 50, 83, 1),
(221, 51, 397, 1),
(222, 51, 398, 1),
(223, 52, 400, 1),
(224, 52, 401, 1),
(225, 53, 395, 1),
(226, 54, 274, 1),
(227, 55, 182, 1),
(228, 56, 315, 1),
(229, 57, 324, 1),
(230, 58, 312, 1),
(231, 59, 340, 1),
(232, 60, 394, 1),
(233, 60, 386, 1),
(238, 62, 88, 1),
(239, 63, 90, 1),
(240, 64, 92, 1),
(241, 64, 93, 1),
(242, 65, 79, 1),
(243, 65, 80, 1),
(244, 66, 88, 1),
(245, 66, 89, 1),
(246, 67, 95, 1),
(247, 67, 96, 1),
(248, 68, 95, 1),
(249, 68, 96, 1),
(250, 69, 89, 1),
(251, 69, 90, 1),
(252, 70, 75, 1),
(253, 70, 76, 1),
(254, 70, 77, 1),
(255, 71, 143, 1),
(256, 71, 144, 1),
(257, 72, 47, 1),
(258, 72, 48, 1),
(259, 72, 38, 1),
(260, 72, 39, 1),
(261, 73, 41, 1),
(262, 73, 42, 1),
(263, 74, 47, 1),
(264, 74, 48, 1),
(265, 75, 27, 1),
(266, 75, 28, 1),
(271, 77, 39, 1),
(272, 77, 40, 1),
(273, 78, 335, 1),
(274, 78, 336, 1),
(275, 79, 443, 0),
(276, 79, 444, 0),
(277, 79, 434, 0),
(278, 80, 134, 0),
(279, 80, 135, 0),
(280, 81, 95, 0),
(281, 81, 96, 0),
(282, 81, 86, 0),
(283, 81, 87, 0),
(284, 81, 88, 0),
(285, 82, 89, 0),
(286, 82, 90, 0),
(287, 82, 91, 0),
(288, 82, 92, 0),
(289, 82, 93, 0),
(290, 83, 73, 0),
(291, 83, 82, 0),
(292, 83, 83, 0),
(293, 83, 84, 0),
(294, 83, 74, 0),
(295, 83, 75, 0),
(296, 83, 76, 0),
(297, 83, 77, 0),
(298, 83, 85, 0),
(299, 83, 94, 0),
(300, 84, 69, 0),
(301, 84, 78, 0),
(302, 84, 79, 0),
(303, 84, 80, 0),
(304, 84, 81, 0),
(305, 85, 49, 0),
(306, 85, 58, 0),
(307, 85, 61, 0),
(308, 85, 70, 0),
(309, 85, 71, 0),
(310, 86, 72, 0),
(311, 86, 62, 0),
(312, 86, 63, 0),
(313, 86, 64, 0),
(314, 86, 65, 0),
(315, 87, 56, 0),
(316, 87, 57, 0),
(317, 87, 66, 0),
(318, 87, 67, 0),
(319, 87, 68, 0),
(320, 88, 52, 0),
(321, 88, 53, 0),
(322, 88, 54, 0),
(323, 88, 55, 0)
;

INSERT INTO booking_transactions (transactionid, transaction_date, transaction_time, no_of_tickets, unit_price, bookingid, ticketid)
VALUES
(1, '2024-01-16', '13:39:36', 1, 20, 1, 1),
(2, '2024-01-16', '13:39:36', 2, 14, 1, 2),
(3, '2024-01-16', '13:49:17', 2, 20, 2, 1),
(4, '2024-01-16', '13:49:17', 1, 16, 2, 3),
(5, '2024-01-16', '13:49:17', 2, 18, 2, 4),
(6, '2024-01-16', '13:52:48', 1, 20, 3, 1),
(7, '2024-01-16', '13:52:48', 2, 14, 3, 2),
(8, '2024-01-28', '11:01:07', 2, 20, 4, 1),
(9, '2024-01-28', '11:01:07', 1, 18, 4, 4),
(10, '2024-01-28', '11:04:26', 1, 20, 5, 1),
(11, '2024-01-28', '11:04:26', 1, 14, 5, 2),
(12, '2024-01-28', '11:04:26', 2, 16, 5, 3),
(13, '2024-01-28', '11:08:20', 5, 16, 6, 3),
(14, '2024-01-28', '11:11:03', 2, 18, 7, 4),
(15, '2024-01-28', '19:23:12', 2, 20, 8, 1),
(16, '2024-01-28', '19:23:12', 2, 18, 8, 4),
(19, '2024-01-29', '14:07:43', 2, 20, 11, 1),
(20, '2024-01-29', '14:07:43', 1, 16, 11, 3),
(21, '2024-01-29', '14:33:38', 1, 20, 12, 1),
(22, '2024-01-29', '14:33:38', 1, 14, 12, 2),
(23, '2024-01-29', '14:37:45', 2, 18, 13, 4),
(25, '2024-01-29', '14:45:17', 1, 20, 15, 1),
(26, '2024-02-03', '20:47:11', 3, 20, 16, 1),
(27, '2024-02-03', '20:47:11', 5, 14, 16, 2),
(28, '2024-02-03', '20:52:14', 5, 16, 17, 3),
(29, '2024-02-03', '20:55:28', 5, 20, 18, 1),
(30, '2024-02-03', '20:55:28', 5, 14, 18, 2),
(31, '2024-02-03', '20:55:28', 5, 16, 18, 3),
(32, '2024-02-03', '21:00:42', 5, 16, 19, 3),
(33, '2024-02-04', '20:54:02', 5, 20, 20, 1),
(34, '2024-02-04', '20:54:02', 5, 16, 20, 3),
(35, '2024-02-04', '20:58:00', 5, 20, 21, 1),
(36, '2024-02-04', '20:58:00', 2, 14, 21, 2),
(37, '2024-02-04', '21:04:39', 5, 10, 22, 5),
(38, '2024-02-04', '21:07:55', 5, 10, 23, 5),
(39, '2024-02-04', '21:12:24', 2, 20, 24, 1),
(40, '2024-02-04', '21:12:24', 4, 14, 24, 2),
(41, '2024-02-04', '21:12:24', 2, 18, 24, 4),
(42, '2024-02-04', '21:20:58', 2, 20, 25, 1),
(43, '2024-02-04', '21:20:58', 2, 16, 25, 3),
(44, '2024-02-04', '21:25:46', 5, 20, 26, 1),
(45, '2024-02-04', '21:25:46', 5, 16, 26, 3),
(46, '2024-02-05', '07:33:46', 5, 20, 27, 1),
(47, '2024-02-05', '07:33:46', 2, 18, 27, 4),
(48, '2024-02-05', '07:37:28', 3, 20, 28, 1),
(49, '2024-02-05', '07:37:28', 3, 16, 28, 3),
(50, '2024-02-05', '07:41:10', 3, 20, 29, 1),
(51, '2024-02-05', '07:41:10', 3, 16, 29, 3),
(52, '2024-02-05', '07:44:27', 5, 20, 30, 1),
(55, '2024-02-05', '07:58:44', 5, 16, 33, 3),
(56, '2024-02-05', '08:01:45', 2, 20, 34, 1),
(57, '2024-02-05', '08:01:45', 2, 18, 34, 4),
(58, '2024-02-05', '08:04:53', 5, 20, 35, 1),
(59, '2024-02-05', '13:31:36', 2, 20, 36, 1),
(60, '2024-02-05', '13:31:36', 2, 16, 36, 3),
(61, '2024-02-05', '13:31:36', 2, 18, 36, 4),
(62, '2024-02-05', '13:35:15', 2, 20, 37, 1),
(66, '2024-02-05', '13:52:56', 2, 14, 40, 2),
(67, '2024-02-05', '13:52:56', 2, 16, 40, 3),
(68, '2024-02-05', '13:58:56', 2, 20, 41, 1),
(69, '2024-02-05', '14:01:37', 5, 10, 42, 5),
(70, '2024-02-05', '14:07:09', 3, 10, 43, 5),
(71, '2024-02-05', '14:11:43', 5, 20, 44, 1),
(72, '2024-02-05', '14:17:17', 3, 10, 45, 5),
(73, '2024-02-06', '11:38:33', 2, 10, 46, 5),
(74, '2024-02-06', '11:43:40', 5, 10, 47, 5),
(75, '2024-02-06', '11:48:25', 1, 10, 48, 5),
(76, '2024-02-06', '11:50:53', 1, 10, 49, 5),
(77, '2024-02-06', '11:54:52', 1, 10, 50, 5),
(78, '2024-02-06', '12:17:00', 2, 20, 51, 1),
(79, '2024-02-06', '12:22:20', 2, 18, 52, 4),
(80, '2024-02-06', '12:24:53', 1, 16, 53, 3),
(81, '2024-02-06', '12:27:44', 1, 16, 54, 3),
(82, '2024-02-06', '12:29:53', 1, 20, 55, 1),
(83, '2024-02-06', '12:44:44', 1, 20, 56, 1),
(84, '2024-02-06', '12:47:11', 1, 16, 57, 3),
(85, '2024-02-06', '12:52:39', 1, 20, 58, 1),
(86, '2024-02-06', '12:55:01', 1, 18, 59, 1),
(87, '2024-02-06', '12:57:33', 2, 18, 60, 4),
(90, '2024-02-06', '13:16:23', 1, 20, 62, 1),
(91, '2024-02-06', '13:18:28', 1, 20, 63, 1),
(92, '2024-02-06', '13:21:44', 2, 16, 64, 3),
(93, '2024-02-06', '13:24:18', 1, 14, 65, 2),
(94, '2024-02-06', '13:24:18', 1, 16, 65, 3),
(95, '2024-02-09', '12:40:19', 2, 16, 66, 3),
(96, '2024-02-09', '12:43:14', 2, 16, 67, 3),
(97, '2024-02-09', '12:46:43', 2, 20, 68, 1),
(98, '2024-02-09', '12:54:55', 2, 18, 69, 4),
(99, '2024-02-09', '12:58:47', 1, 20, 70, 1),
(100, '2024-02-09', '12:58:47', 2, 14, 70, 2),
(101, '2024-02-09', '13:03:35', 2, 20, 71, 1),
(102, '2024-02-09', '13:06:00', 2, 14, 72, 2),
(103, '2024-02-09', '13:06:00', 2, 18, 72, 4),
(104, '2024-02-09', '13:10:01', 2, 16, 73, 3),
(105, '2024-02-09', '13:12:30', 2, 20, 74, 1),
(106, '2024-02-09', '13:18:12', 2, 16, 75, 3),
(109, '2024-02-09', '14:54:03', 2, 20, 77, 1),
(110, '2024-02-09', '14:58:19', 2, 10, 78, 5),
(111, '2024-02-11', '20:59:15', 3, 20, 79, 1),
(112, '2024-02-11', '21:02:23', 2, 20, 80, 1),
(113, '2024-02-11', '21:30:55', 5, 20, 81, 1),
(114, '2024-02-11', '21:34:17', 5, 16, 82, 3),
(115, '2024-02-11', '21:38:42', 5, 20, 83, 1),
(116, '2024-02-11', '21:38:42', 5, 14, 83, 2),
(117, '2024-02-11', '21:41:13', 5, 14, 84, 2),
(118, '2024-02-11', '21:44:47', 5, 20, 85, 1),
(119, '2024-02-11', '21:47:23', 5, 14, 86, 2),
(120, '2024-02-11', '21:59:06', 5, 20, 87, 1),
(121, '2024-02-11', '22:01:48', 4, 16, 88, 3)
;

INSERT INTO payment (paymentid, amount, payment_date, payment_time, payment_type, customerid, bookingid)
VALUES
(1, 48, '2024-01-16', '13:39:36', 'booking', 2, 1),
(2, 92, '2024-01-16', '13:49:17', 'booking', 1, 2),
(3, 48, '2024-01-16', '13:52:48', 'booking', 131, 3),
(4, 58, '2024-01-28', '11:01:07', 'booking', 1, 4),
(5, 66, '2024-01-28', '11:04:26', 'booking', 4, 5),
(6, 80, '2024-01-28', '11:08:20', 'booking', 5, 6),
(7, 36, '2024-01-28', '11:11:03', 'booking', 6, 7),
(10, 76, '2024-01-28', '19:23:12', 'booking', 7, 8),
(14, 56, '2024-01-29', '14:07:43', 'booking', 2, 11),
(18, 34, '2024-01-29', '14:33:38', 'booking', 13, 12),
(19, 36, '2024-01-29', '14:37:45', 'booking', 20, 13),
(21, 20,'2024-01-29', '14:45:17', 'booking', 138, 15),
(22, 130, '2024-02-03', '20:47:11', 'booking', 21, 16),
(23, 80, '2024-02-03', '20:52:14', 'booking', 144, 17),
(24, 250, '2024-02-03', '20:55:28', 'booking', 27, 18),
(25, 80, '2024-02-03', '21:00:42', 'booking', 37, 19),
(26, 180, '2024-02-04', '20:54:02', 'booking', 8, 20),
(27, 128, '2024-02-04', '20:58:00', 'booking', 11, 21),
(29, 50, '2024-02-04', '21:04:39', 'booking', 13, 22),
(30, 50, '2024-02-04', '21:07:55', 'booking', 13, 23),
(31, 132, '2024-02-04', '21:12:24', 'booking', 2, 24),
(32, 72, '2024-02-04', '21:20:58', 'booking', 22, 25),
(33, 180, '2024-02-04', '21:25:46', 'booking', 15, 26),
(35, 136, '2024-02-05', '07:33:46', 'booking', 10, 27),
(36, 108, '2024-02-05', '07:37:28', 'booking', 17, 28),
(37, 108, '2024-02-05', '07:41:10', 'booking', 17, 29),
(38, 100, '2024-02-05', '07:44:27', 'booking', 16, 30),
(43, 80, '2024-02-05', '07:58:44', 'booking', 17, 33),
(44, 76, '2024-02-05', '08:01:45', 'booking', 20, 34),
(45, 100, '2024-02-05', '08:04:53', 'booking', 21, 35),
(48, 108, '2024-02-05', '13:31:36', 'booking', 25, 36),
(49, 40, '2024-02-05', '13:35:15', 'booking', 25, 37),
(52, 60, '2024-02-05', '13:52:56', 'booking', 39, 40),
(53, 40, '2024-02-05', '13:58:56', 'booking', 40, 41),
(54, 50, '2024-02-05', '14:01:37', 'booking', 44, 42),
(55, 30, '2024-02-05', '14:07:09', 'booking', 45, 43),
(56, 100, '2024-02-05', '14:11:43', 'booking', 48, 44),
(57, 30, '2024-02-05', '14:17:17', 'booking', 55, 45),
(58, 20, '2024-02-06', '11:38:33', 'booking', 46, 46),
(60, 50, '2024-02-06', '11:43:40', 'booking', 51, 47),
(61, 10, '2024-02-06', '11:48:25', 'booking', 53, 48),
(62, 10, '2024-02-06', '11:50:53', 'booking', 56, 49),
(63, 10, '2024-02-06', '11:54:52', 'booking', 60, 50),
(64, 40, '2024-02-06', '12:17:00', 'booking', 83, 51),
(66, 36, '2024-02-06', '12:22:20', 'booking', 85, 52),
(67, 16, '2024-02-06', '12:24:53', 'booking', 97, 53),
(68, 16, '2024-02-06', '12:27:44', 'booking', 98, 54),
(69, 20, '2024-02-06', '12:29:53', 'booking', 99, 55),
(70, 20, '2024-02-06', '12:44:44', 'booking', 112, 56),
(71, 16, '2024-02-06', '12:47:11', 'booking', 113, 57),
(72, 20, '2024-02-06', '12:52:39', 'booking', 14, 58),
(73, 18, '2024-02-06', '12:55:01', 'booking', 20, 59),
(74, 36, '2024-02-06', '12:57:33', 'booking', 11, 60),
(77, 20, '2024-02-06', '13:16:23', 'booking', 42, 62),
(78, 20, '2024-02-06', '13:18:28', 'booking', 41, 63),
(79, 32, '2024-02-06', '13:21:44', 'booking', 21, 64),
(80, 30, '2024-02-06', '13:24:18', 'booking', 31, 65),
(81, 32, '2024-02-09', '12:40:19', 'booking', 63, 66),
(82, 32, '2024-02-09', '12:43:14', 'booking', 65, 67),
(83, 40, '2024-02-09', '12:46:43', 'booking', 75, 68),
(84, 36, '2024-02-09', '12:54:55', 'booking', 66, 69),
(85, 48, '2024-02-09', '12:58:47', 'booking', 83, 70),
(87, 40, '2024-02-09', '13:03:35', 'booking', 68, 71),
(88, 64, '2024-02-09', '13:06:00', 'booking', 77, 72),
(89, 32, '2024-02-09', '13:10:01', 'booking', 25, 73),
(90, 40, '2024-02-09', '13:12:30', 'booking', 38, 74),
(92, 32, '2024-02-09', '13:18:12', 'booking', 44, 75),
(94, 40, '2024-02-09', '14:54:03', 'booking', 25, 77),
(95, 20, '2024-02-09', '14:58:19', 'booking', 32, 78),
(97, 60, '2024-02-11', '20:59:15', 'booking', 1, 79),
(98, 40, '2024-02-11', '21:02:23', 'booking', 76, 80),
(100, 100, '2024-02-11', '21:30:55', 'booking', 83, 81),
(101, 80, '2024-02-11', '21:34:17', 'booking', 86, 82),
(102, 170, '2024-02-11', '21:38:42', 'booking', 92, 83),
(103, 70, '2024-02-11', '21:41:13', 'booking', 105, 84),
(104, 100, '2024-02-11', '21:44:47', 'booking', 111, 85),
(105, 70, '2024-02-11', '21:47:23', 'booking', 115, 86),
(106, 100, '2024-02-11', '21:59:06', 'booking', 95, 87),
(107, 64, '2024-02-11', '22:01:48', 'booking', 70, 88)
;

INSERT INTO payment (paymentid, amount, payment_date, payment_time, payment_type, customerid, bookingid)
VALUES
(8, 100, '2024-01-18', '11:19:27', 'giftcard', 6, NULL),
(9, 100, '2024-01-18', '11:25:02', 'giftcard', 1, NULL),
(11, 150, '2024-01-18', '19:32:32', 'giftcard', 7, NULL),
(15, 150, '2024-01-29', '14:10:57', 'giftcard', 2, NULL),
(16, 100, '2024-01-29', '14:14:25', 'giftcard', 9, NULL),
(17, 20, '2024-01-29', '14:17:10', 'giftcard', 9, NULL),
(28, 90, '2024-02-04', '21:01:19', 'giftcard', 11, NULL),
(34, 160, '2024-02-05', '07:30:53', 'giftcard', 10, NULL),
(39, 250, '2024-02-05', '07:47:10', 'giftcard', 16, NULL),
(42, 300, '2024-02-05', '07:55:51', 'giftcard', 9, NULL),
(46, 200, '2024-02-05', '08:07:31', 'giftcard', 21, NULL),
(47, 40, '2024-02-05', '08:09:23', 'giftcard', 21, NULL),
(59, 100, '2024-02-06', '11:41:19', 'giftcard', 46, NULL),
(65, 125, '2024-02-06', '12:19:56', 'giftcard', 83, NULL),
(75, 50, '2024-02-06', '12:59:35', 'giftcard', 121, NULL),
(86, 100, '2024-02-09', '13:01:21', 'giftcard', 83, NULL),
(91, 30, '2024-02-09', '13:16:16', 'giftcard', 38, NULL),
(96, 50, '2024-02-09', '15:01:53', 'giftcard', 32, NULL),
(99, 100, '2024-02-11', '21:05:19', 'giftcard', 76, NULL),
(108, 50, '2024-02-11', '22:05:09', 'giftcard', 70, NULL)
;

INSERT INTO giftcards (giftcardid, giftcard_number, giftcard_value, giftcard_type_id, customerid)
VALUES
(1, 'H1pXwaPJ3eI2EFZc', 50, 2, 6),
(2, 'L6cJcv8ysqwTMf0e', 50, 2, 6),
(3, 'T27fT1eH8liIAz7k', 100, 3, 1),
(4, 'b877A4GI5l5rpgdO', 50, 2, 7),
(5, 'm0YcFZlDvjn9pCAq', 50, 2, 7),
(6, 'jdttBA2FzqQufhIh', 50, 2, 7),
(7, 'Sz7xkgru8utM7PwL', 50, 2, 2),
(8, 'cOnocD1KhpmymYEL', 50, 2, 2),
(9, 'nUymT1GOmORsQmIS', 50, 2, 2),
(10, 'T6zUBDBXLZ2FdWPd', 100, 1, 9),
(11, '9g1qKXT4IfINW4rU', 20, 3, 9),
(12, 'jfTla5ASPno6O2WH', 30, 2, 11),
(13, 'wQSUDWyyxOhUcuHM', 30, 2, 11),
(14, 'v2CUBQDcd8E7mqH5', 30, 2, 11),
(15, 'saY1DkszohxasiBx', 80, 1, 10),
(16, 'jt6tJh0OMJhUWuna', 80, 1, 10),
(17, 'p4GpIu6IbNzbKhpg', 250, 2, 16),
(18, 'owvYd24C8aDfkEDk', 150, 2, 9),
(19, 'VlkAw1LBJZQvAvy2', 150, 2, 9),
(20, 'wT8QFfAPX5EeqPmr', 200, 1, 21),
(21, '1omFyRVI7ZAVHiwI', 20, 3, 21),
(22, 'sKUoO0udTFsYAKZG', 20, 3, 21),
(23, 'OWDQPmqwSpfGnjRV', 50, 4, 46),
(24, 'xyP8oYFY5JApbwWh', 50, 4, 46),
(25, 'k6lUJJ6058PL5GxF', 125, 4, 83),
(26, 'QvCIdllu2qbgJiYz', 50, 2, 121),
(27, 'MpSjFLxRcBgNf0Rl', 100, 4, 83),
(28, 'Awt2HM8pa5tWQxvG', 30, 1, 38),
(29, 'B0skM2NXxXq0EbYX', 50, 1, 32),
(30, '40VNO7UpS7c01Ypa', 100, 2, 76),
(31, 'qvWIgDFxjItoIR9K', 50, 2, 70)
;

INSERT INTO giftcard_payment (gpid, giftcardid, paymentid)
VALUES
(1, 1, 8),
(2, 2, 8),
(3, 3, 9),
(4, 4, 11),
(5, 5, 11),
(6, 6, 11),
(7, 7, 15),
(8, 8, 15),
(9, 9, 15),
(10, 10, 16),
(11, 11, 17),
(12, 12, 28),
(13, 13, 28),
(14, 14, 28),
(15, 15, 34),
(16, 16, 34),
(17, 17, 39),
(18, 18, 42),
(19, 19, 42),
(20, 20, 46),
(21, 21, 47),
(22, 22, 47),
(23, 23, 59),
(24, 24, 59),
(25, 25, 65),
(26, 26, 75),
(27, 27, 86),
(28, 28, 91),
(29, 29, 96),
(30, 30, 99),
(31, 31, 108)
;

-- bookings with giftcard applied
INSERT INTO bookings (bookingid, booking_date, booking_time, no_of_tickets, total_amount, giftcardid, giftcard_deducted, payment_amount, customerid, sessionid)
VALUES
(9, '2024-01-18', '19:35:03', 2, 28, 4, 28, 0, 7, 295),
(10, '2024-01-18', '19:35:58', 2, 40, 4, 22, 18, 7, 304),
(14, '2024-01-29', '14:41:58', 2, 32, 11, 20, 12, 20, 292),
(31, '2024-02-05', '07:49:32', 3, 48, 10, 48, 0, 9, 400),
(32, '2024-02-05', '07:52:44', 5, 80, 10, 52, 28, 9, 414),
(38, '2024-02-05', '13:42:15', 5, 100, 7, 50, 50, 29, 400),
(39, '2024-02-05', '13:45:50', 4, 72, 8, 50, 22, 29, 234),
(61, '2024-02-06', '13:11:52', 4, 76, 18, 76, 0, 126, 410),
(76, '2024-02-09', '13:22:11', 4, 76, 24, 50, 26, 14, 431)
;

INSERT INTO booking_seats (bsid, bookingid, seatid, is_checkin)
VALUES
(30, 9, 93, 1),
(31, 9, 94, 1),
(32, 10, 90, 1),
(33, 10, 91, 1),
(41, 14, 29, 1),
(42, 14, 30, 1),
(150, 31, 363, 1),
(151, 31, 365, 1),
(152, 31, 374, 1),
(153, 32, 387, 1),
(154, 32, 388, 1),
(155, 32, 389, 1),
(156, 32, 390, 1),
(157, 32, 391, 1),
(180, 38, 313, 1),
(181, 38, 315, 1),
(182, 38, 324, 1),
(183, 38, 316, 1),
(184, 38, 317, 1),
(185, 39, 91, 1),
(186, 39, 92, 1),
(187, 39, 93, 1),
(188, 39, 94, 1),
(234, 61, 135, 1),
(235, 61, 136, 1),
(236, 61, 137, 1),
(237, 61, 138, 1),
(267, 76, 407, 1),
(268, 76, 408, 1),
(269, 76, 398, 1),
(270, 76, 399, 1)
;

INSERT INTO booking_transactions (transactionid, transaction_date, transaction_time, no_of_tickets, unit_price, bookingid, ticketid)
VALUES
(17, '2024-01-18', '19:35:03', 2, 14, 9, 2),
(18, '2024-01-18', '19:35:58', 2, 20, 10, 1),
(24, '2024-01-29', '14:41:58', 2, 16, 14, 3),
(53, '2024-02-05', '07:49:32', 3, 16, 31, 3),
(54, '2024-02-05', '07:52:44', 5, 16, 32, 3),
(63, '2024-02-05', '13:42:15', 5, 20, 38, 1),
(64, '2024-02-05', '13:45:50', 2, 20, 39, 1),
(65, '2024-02-05', '13:45:50', 2, 16, 39, 3),
(88, '2024-02-06', '13:11:52', 2, 20, 61, 1),
(89, '2024-02-06', '13:11:52', 2, 18, 61, 4),
(107, '2024-02-09', '13:22:11', 2, 20, 76, 1),
(108, '2024-02-09', '13:22:11', 2, 18, 76, 4)
;

INSERT INTO payment (paymentid, amount, payment_date, payment_time, payment_type, customerid, bookingid)
VALUES
(12, 0, '2024-01-18', '19:35:03', 'booking', 7, 9),
(13, 18, '2024-01-18', '19:35:58', 'booking', 7, 10),
(20, 12, '2024-01-29', '14:41:58', 'booking', 20, 14),
(40, 0, '2024-02-05', '07:49:32', 'booking', 9, 31),
(41, 28, '2024-02-05', '07:52:44', 'booking', 9, 32),
(50, 50, '2024-02-05', '13:42:15', 'booking', 29, 38),
(51, 22, '2024-02-05', '13:45:50', 'booking', 29, 39),
(76, 0, '2024-02-06', '13:11:52', 'booking', 126, 61),
(93, 26, '2024-02-09', '13:22:11', 'booking', 14, 76)

