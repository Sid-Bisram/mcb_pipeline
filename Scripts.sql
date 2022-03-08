CREATE DATABASE db_hp;

CREATE TABLE `happiness_report_maintable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) DEFAULT NULL,
  `happiness_score` double DEFAULT NULL,
  `standard_error` double DEFAULT NULL,
  `lower_limit` double DEFAULT NULL,
  `upper_limit` double DEFAULT NULL,
  `economy_gdp` double DEFAULT NULL,
  `family` double DEFAULT NULL,
  `health_life_expectancy` double DEFAULT NULL,
  `freedom` double DEFAULT NULL,
  `trust` double DEFAULT NULL,
  `generosity` double DEFAULT NULL,
  `dystopia_residual` double DEFAULT NULL,
  `report_year` int(11) DEFAULT NULL COMMENT 'year from which report has been issued',
  `date_created` datetime DEFAULT current_timestamp(),
  `date_modified` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1024 DEFAULT CHARSET=latin1;

CREATE TABLE `happiness_report_sourcetable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(150) DEFAULT NULL,
  `happiness_score` double DEFAULT NULL,
  `standard_error` double DEFAULT NULL,
  `lower_limit` double DEFAULT NULL,
  `upper_limit` double DEFAULT NULL,
  `economy_gdp` double DEFAULT NULL,
  `family` double DEFAULT NULL,
  `health_life_expectancy` double DEFAULT NULL,
  `freedom` double DEFAULT NULL,
  `trust` double DEFAULT NULL,
  `generosity` double DEFAULT NULL,
  `dystopia_residual` double DEFAULT NULL,
  `report_year` int(11) DEFAULT NULL COMMENT 'year from which report has been issued',
  `date_created` datetime DEFAULT current_timestamp(),
  `date_modified` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=783 DEFAULT CHARSET=latin1;

CREATE TABLE `tbl_country_region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` text DEFAULT NULL,
  `images_file` text DEFAULT NULL,
  `image_url` text DEFAULT NULL,
  `alpha_2` text DEFAULT NULL,
  `alpha_3` text DEFAULT NULL,
  `country_code` double DEFAULT NULL,
  `iso_3166_2` text DEFAULT NULL,
  `region` text DEFAULT NULL,
  `sub_region` text DEFAULT NULL,
  `intermediate_region` text DEFAULT NULL,
  `region_code` double DEFAULT NULL,
  `sub_region_code` double DEFAULT NULL,
  `intermediate_region_code` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `capital_city` text DEFAULT NULL,
  `date_created` datetime DEFAULT current_timestamp(),
  `date_modified` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=274 DEFAULT CHARSET=latin1;

DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `report_3`(arg_report_year int,arg_country varchar(150))
BEGIN
	SELECT main.report_year,country.country,country.image_url,country.region_code,case when country.region is null or country.region = '' then 'Nan' else UPPER(country.region) end as region,
	rank_per_region(country.region,country.country, main.report_year) as ranking_per_region,
	overall_rank(country.country, main.report_year) as overall_ranking,
	main.happiness_score,
	case when main.happiness_score>5.6 then 'Green' else case when main.happiness_score>=2.6 and main.happiness_score<5.6 then 'Amber' else 'Red' end end as Happiness_Status,
	main.economy_gdp,
	main.family,
	main.family as Social_support,
	main.health_life_expectancy,
	main.freedom,
	main.Generosity,
	main.trust
	FROM db_hp.happiness_report_maintable main
	left join tbl_country_region country on main.country_id=country.id
    where main.report_year=arg_report_year and country.country=arg_country;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`%` FUNCTION `overall_rank`(arg_country varchar(150),arg_report_year int) RETURNS int(11)
BEGIN
	DECLARE ranking int;

	WITH order_values AS(
    SELECT DISTINCT
        country.country,
        main.report_year,
        main.happiness_score,
        RANK() OVER (
            PARTITION BY YEAR(main.report_year)
            ORDER BY main.happiness_score DESC
        ) order_value_rank
    from happiness_report_maintable main
	left join tbl_country_region country on main.country_id=country.id
     WHERE 
     main.report_year=arg_report_year
	)

	SELECT 
		order_value_rank into ranking
	FROM 
		order_values
	where country=arg_country
	;
    return ranking;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`%` FUNCTION `rank_per_region`(arg_region varchar(150),arg_country varchar(150),arg_report_year int) RETURNS int(11)
BEGIN
	DECLARE ranking int;

	WITH order_values AS(
    SELECT 
        country.region,
        country.country,
        main.report_year,
        main.happiness_score,
        RANK() OVER (
            PARTITION BY YEAR(main.report_year)
            ORDER BY main.happiness_score DESC
        ) order_value_rank
    from happiness_report_maintable main
	left join tbl_country_region country on main.country_id=country.id
     WHERE 
     country.region=arg_region and main.report_year=arg_report_year
	)

	SELECT 
		order_value_rank into ranking
	FROM 
		order_values
	where country=arg_country
	;
    return ranking;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `report_4`(arg_country varchar(150))
BEGIN
	WITH order_values AS(
		SELECT 
			country.country,
			main.report_year,
			main.happiness_score,
			RANK() OVER (
				PARTITION BY YEAR(main.report_year)
				ORDER BY main.happiness_score DESC
			) order_value_rank
		from happiness_report_maintable main
		left join tbl_country_region country on main.country_id=country.id
	)

	SELECT
		country,
		min(order_value_rank) as highest_rank, 
        max(order_value_rank) as lowest_rank,
        max(happiness_score) as highest_score,
        min(happiness_score) as lowest_score
        from
		order_values
	where country=arg_country;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `transfer_to_maintable`()
BEGIN
	INSERT INTO `db_hp`.`happiness_report_maintable`
	(`country_id`,
	`happiness_score`,
	`standard_error`,
	`lower_limit`,
	`upper_limit`,
	`economy_gdp`,
	`family`,
	`health_life_expectancy`,
	`freedom`,
	`trust`,
	`generosity`,
	`dystopia_residual`,
	`report_year`)
	SELECT country.id as country_id,src.happiness_score,src.standard_error,src.lower_limit,src.upper_limit,src.economy_gdp,src.family,src.health_life_expectancy,src.freedom,src.trust,src.generosity
	,src.dystopia_residual,src.report_year 
	FROM db_hp.happiness_report_sourcetable src
	left join tbl_country_region country on src.country=country.country
	left join db_hp.happiness_report_maintable main on country.id=main.country_id and src.report_year=main.report_year
	where main.id is null and country.id is not null
	order by src.report_year;
END$$
DELIMITER ;

