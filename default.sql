CREATE TABLE IF NOT EXISTS `guilds`(
    `id` int(20) NOT NULL,
    PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `products`(
    `server_id` int(20) NOT NULL,
    `uuid` VARCHAR(40) NOT NULL PRIMARY KEY,
    `name` VARCHAR(30) NOT NULL,
    `price` int(10) NOT NULL,
    `description` VARCHAR(100) NOT NULL DEFAULT '',
    FOREIGN KEY (`server_id`) REFERENCES `guilds`(`id`)
);

