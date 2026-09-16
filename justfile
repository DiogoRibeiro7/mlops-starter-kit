# https://just.systems/man/en/

set dotenv-load := true

PACKAGE := "mlops_starter_kit"
SOURCES := "src"
TESTS := "tests"

default:
    @just --list

import 'tasks/check.just'
import 'tasks/clean.just'
import 'tasks/docker.just'
import 'tasks/docs.just'
import 'tasks/format.just'
import 'tasks/install.just'
import 'tasks/package.just'
import 'tasks/project.just'
