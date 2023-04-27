-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- 主機: 127.0.0.1
-- 產生時間： 2018 年 06 月 08 日 17:41
-- 伺服器版本: 10.1.32-MariaDB
-- PHP 版本： 7.2.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `album`
--

-- --------------------------------------------------------

--
-- 資料表結構 `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(24) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `account` varchar(24) NOT NULL,
  `password` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 資料表的匯出資料 `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `account`, `password`) VALUES
(1, '示範用', 'chi', 'chi');

-- --------------------------------------------------------

--
-- 資料表結構 `pictures`
--

CREATE TABLE `pictures` (
  `id` int(11) NOT NULL,
  `account` varchar(24) NOT NULL,
  `albumid` int(11) NOT NULL DEFAULT '-1',
  `pic0` int(11) NOT NULL DEFAULT '0',
  `pic1` int(11) NOT NULL DEFAULT '0',
  `pic2` int(11) NOT NULL DEFAULT '0',
  `pic3` int(11) NOT NULL DEFAULT '0',
  `pic4` int(11) NOT NULL DEFAULT '0',
  `pic5` int(11) NOT NULL DEFAULT '0',
  `pic6` int(11) NOT NULL DEFAULT '0',
  `pic7` int(11) NOT NULL DEFAULT '0',
  `pic8` int(11) NOT NULL DEFAULT '0',
  `pic9` int(11) NOT NULL DEFAULT '0',
  `pic10` int(11) NOT NULL DEFAULT '0',
  `pic11` int(11) NOT NULL DEFAULT '0',
  `pic12` int(11) NOT NULL DEFAULT '0',
  `pic13` int(11) NOT NULL DEFAULT '0',
  `pic14` int(11) NOT NULL DEFAULT '0',
  `aname` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT 'None'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 資料表的匯出資料 `pictures`
--

INSERT INTO `pictures` (`id`, `account`, `albumid`, `pic0`, `pic1`, `pic2`, `pic3`, `pic4`, `pic5`, `pic6`, `pic7`, `pic8`, `pic9`, `pic10`, `pic11`, `pic12`, `pic13`, `pic14`, `aname`) VALUES
(1, 'chi', 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '玩具總動員'),
(2, 'chi', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '海底總動員'),
(3, 'chi', 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '怪獸電力公司'),
(4, 'chi', 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '鋼鐵人'),
(5, 'chi', 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'KITTY'),
(6, 'chi', 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '小小兵'),
(7, 'chi', 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '萬獸之王'),
(8, 'chi', 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '瘋狂原始人');

--
-- 已匯出資料表的索引
--

--
-- 資料表索引 `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `pictures`
--
ALTER TABLE `pictures`
  ADD PRIMARY KEY (`id`);

--
-- 在匯出的資料表使用 AUTO_INCREMENT
--

--
-- 使用資料表 AUTO_INCREMENT `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表 AUTO_INCREMENT `pictures`
--
ALTER TABLE `pictures`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
