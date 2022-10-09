--EX: INSERT INTO products (uuid, guild_uuid, name, price, description, date) VALUES ("12323112114541123123454542331", "b2b6768e-1442-46ee-b325-27358094fdf6", "fortnite4", 12, "fortnite11", 123123)

CREATE TABLE IF NOT EXISTS `guilds`(
    `uuid` VARCHAR(40) NOT NULL, -- random
    `id` int(20) NOT NULL, --server id 
    `date` int(30) NOT NULL,

    PRIMARY KEY (`uuid`)
);

CREATE TABLE IF NOT EXISTS `products`(
    `uuid` VARCHAR(40) NOT NULL,
    `guild_uuid` int(20) NOT NULL,
    `name` VARCHAR(30) NOT NULL,
    `price` int(10) NOT NULL,
    `description` VARCHAR(100) NOT NULL DEFAULT '',
    `date` int(30) NOT NULL,

    PRIMARY KEY (`uuid`),
    FOREIGN KEY (`guild_uuid`) REFERENCES `guilds`(`uuid`) ON DELETE CASCADE ON UPDATE CASCADE --if guild is deleted, delete all products of the guild
);


CREATE TABLE IF NOT EXISTS `customers`(
    `uuid` VARCHAR(40) NOT NULL, --random id
    `id` int(20) NOT NULL, --discord user id
    `guild_uuid` int(20) NOT NULL, --server id
    `product_uuid` VARCHAR(40) NOT NULL, --product id SEE table products `uuid`
    `date` int(30) NOT NULL, --date time for logging (when customer was created)

    PRIMARY KEY (`uuid`),
    FOREIGN KEY (`guild_uuid`) REFERENCES `guilds`(`uuid`) ON DELETE CASCADE ON UPDATE CASCADE, --if guild is deleted, delete all customers of the guild
    FOREIGN KEY (`product_uuid`) REFERENCES `products`(`uuid`) ON DELETE CASCADE ON UPDATE CASCADE --if product is deleted, delete all customers of the product
);

CREATE TABLE IF NOT EXISTS `licenses`(
    `uuid` VARCHAR(40) NOT NULL, --Public Key
    `license` VARCHAR(80) NOT NULL, --Private Key
    `product_uuid` VARCHAR(40) NOT NULL, --Product UUID SEE table products `uuid`
    `customer_uuid` VARCHAR(40) NOT NULL, --Customer UUID SEE table customers `uuid`
    `date` int(30) NOT NULL,

    PRIMARY KEY (`uuid`),
    FOREIGN KEY (`customer_uuid`) REFERENCES `customers`(`uuid`) ON DELETE CASCADE ON UPDATE CASCADE, --if customer is deleted, delete license
    FOREIGN KEY (`product_uuid`) REFERENCES `products`(`uuid`) ON DELETE CASCADE ON UPDATE CASCADE -- if product is deleted, delete license
);






