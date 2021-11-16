#!/usr/bin/env bash

echo "Initializing conda in dev mode..."
echo "Factory config is:"
grep -e "conda location" -e "conda version" -e "python version" <(conda info -a) | sed 's/^\s*/  /'
eval "$(sudo /opt/conda/bin/python -m conda init --dev bash)"
echo "Done! Now running:"
grep -e "conda location" -e "conda version" -e "python version" <(conda info -a) | sed 's/^\s*/  /'
