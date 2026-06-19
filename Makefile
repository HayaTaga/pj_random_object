.DEFAULT_GOAL := help

TOPIC ?=
TITLE ?=
DATE ?= $(shell date +%F)

.PHONY: help topic note papers

help:
	@printf "%s\n" "Usage:"
	@printf "%s\n" "  make topic TOPIC=theme_name"
	@printf "%s\n" "  make note TITLE=short_title"
	@printf "%s\n" "  make papers"
	@printf "%s\n" ""
	@printf "%s\n" "Examples:"
	@printf "%s\n" "  make topic TOPIC=random_sets"
	@printf "%s\n" "  make note TITLE=random_closed_sets"

topic:
	@test -n "$(TOPIC)" || { echo "ERROR: set TOPIC=snake_case_name"; exit 1; }
	@case "$(TOPIC)" in *[!a-z0-9_]*|_*|*_) echo "ERROR: TOPIC must be snake_case, e.g. random_sets"; exit 1;; esac
	@test ! -e "topics/$(TOPIC)" || { echo "ERROR: topics/$(TOPIC) already exists"; exit 1; }
	@cp -R topics/_template "topics/$(TOPIC)"
	@sed -i.bak "s/# Theme Title/# $(TOPIC)/" "topics/$(TOPIC)/README.md"
	@rm "topics/$(TOPIC)/README.md.bak"
	@echo "created topics/$(TOPIC)"

note:
	@test -n "$(TITLE)" || { echo "ERROR: set TITLE=snake_case_title"; exit 1; }
	@case "$(TITLE)" in *[!a-z0-9_]*|_*|*_) echo "ERROR: TITLE must be snake_case, e.g. random_closed_sets"; exit 1;; esac
	@test ! -e "notes/$(DATE)_$(TITLE).md" || { echo "ERROR: notes/$(DATE)_$(TITLE).md already exists"; exit 1; }
	@cp notes/_template.md "notes/$(DATE)_$(TITLE).md"
	@sed -i.bak "s/# Title/# $(TITLE)/; s/date:/date: $(DATE)/" "notes/$(DATE)_$(TITLE).md"
	@rm "notes/$(DATE)_$(TITLE).md.bak"
	@echo "created notes/$(DATE)_$(TITLE).md"

papers:
	@test -d papers || { echo "ERROR: papers/ does not exist"; exit 1; }
	@find papers -maxdepth 1 -type f -name '*.pdf' -print | sort
