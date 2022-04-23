docker run --mount type=bind,source="$(pwd)"/,target=/app node /bin/bash -c "apt update && apt install zip && cd app && rm -r dist && yarn && yarn dist && cd dist && zip -r dist.zip ./"
