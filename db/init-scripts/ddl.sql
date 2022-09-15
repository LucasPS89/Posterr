CREATE TABLE if not exists `user`(
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `username` varchar(14) NOT NULL,
    `date_joined` DATE not null default(CURRENT_DATE),
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE if not exists `post`(
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `repost_from_id` bigint(20), 
    `quote_from_id` bigint(20), 
    `user_id` bigint(20),
    `datetime_creation` TIMESTAMP NOT NULL DEFAULT(CURRENT_TIMESTAMP),
    `text` varchar(777),
    PRIMARY KEY (id),
    FOREIGN KEY (repost_from_id) REFERENCES post(id),
    FOREIGN KEY (quote_from_id) REFERENCES post(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    INDEX (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Sample Data*/
insert into user (username) values ('Carol');
insert into user (username) values ('John');
insert into user (username) values ('Elizabeth99');

insert into post (user_id, text) values (1, 'Hello World');
insert into post (user_id, text, repost_from_id) values (2, 'Take a look of what Carol is posting', 1);
insert into post (user_id, text, quote_from_id) values (2, 'Quoting what Carol said', 1);

