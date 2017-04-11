-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema paycheck_calculator
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema paycheck_calculator
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `paycheck_calculator` DEFAULT CHARACTER SET utf8 ;
USE `paycheck_calculator` ;

-- -----------------------------------------------------
-- Table `paycheck_calculator`.`federal_tax_bracket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `paycheck_calculator`.`federal_tax_bracket` (
  `RATE` DOUBLE NULL DEFAULT NULL,
  `STATUS` CHAR(50) NULL DEFAULT NULL,
  `MIN` DOUBLE NULL DEFAULT NULL,
  `MAX` DOUBLE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `paycheck_calculator`.`state_tax_bracket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `paycheck_calculator`.`state_tax_bracket` (
  `STATE` CHAR(50) NULL DEFAULT NULL,
  `RATE` DOUBLE NULL DEFAULT NULL,
  `STATUS` CHAR(50) NULL DEFAULT NULL,
  `MIN` DOUBLE NULL DEFAULT NULL,
  `MAX` DOUBLE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
