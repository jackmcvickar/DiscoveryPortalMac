# Makefile

.PHONY: run-pipeline

run-pipeline:
	@echo "Running ingestion pipeline..."
	python pipeline.py
