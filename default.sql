CREATE TABLE IF NOT EXISTS `guilds`(
    `uuid` VARCHAR(40) NOT NULL, -- random
    `id` int(20) NOT NULL, --server id 
    `date` DATETIME NOT NULL,
    PRIMARY KEY (`uuid`)
);

CREATE TABLE IF NOT EXISTS `products`(
    `uuid` VARCHAR(40) NOT NULL,
    `server_uuid` int(20) NOT NULL,
    `name` VARCHAR(30) NOT NULL,
    `price` int(10) NOT NULL,
    `description` VARCHAR(100) NOT NULL DEFAULT '',
    PRIMARY KEY (`uuid`),
    FOREIGN KEY (`server_uuid`) REFERENCES `guilds`(`uuid`)
);

CREATE TABLE IF NOT EXISTS `licenses`(
    `uuid` VARCHAR(40) NOT NULL, --Public Key
    `license` VARCHAR(80) NOT NULL, --Private Key
    `product_uuid` VARCHAR(40) NOT NULL, --Product UUID SEE table products `uuid`
    `date` DATETIME NOT NULL,

    PRIMARY KEY (`uuid`),
    FOREIGN KEY (`product_uuid`) REFERENCES `products`(`uuid`) ON DELETE CASCADE ON UPDATE CASCADE
);








CREATE TABLE IF NOT EXISTS `customers`(
    `uuid` VARCHAR(40) NOT NULL, --random id
    `customer_uuid` int(20) NOT NULL, --discord user id
    `server_uuid` int(20) NOT NULL, --server id
    `product_uuid` VARCHAR(40) NOT NULL, --product id SEE table products `uuid`
    `date` DATETIME NOT NULL, --date time for logging (when customer was created)
    PRIMARY KEY (`uuid`),
    FOREIGN KEY (`server_uuid`) REFERENCES `guilds`(`uuid`),
    FOREIGN KEY (`product_uuid`) REFERENCES `products`(`uuid`)
);