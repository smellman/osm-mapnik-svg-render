FROM debian:bookworm

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-mapnik \
    curl \
    git \
    wget \
    node-carto \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Clone openstreetmap-carto
WORKDIR /src
RUN git clone https://github.com/gravitystorm/openstreetmap-carto.git
WORKDIR /src/openstreetmap-carto
# Edit scripts/get-fonts.sh to download the fonts
RUN sed -i 's|https://fonts.google.com/download?family=Noto%20Emoji|https://file.smellman.org/Noto_Emoji.zip|g' scripts/get-fonts.sh
RUN sh scripts/get-fonts.sh
# Edit the project file to connect postgresql
COPY project.mml.patch /src/openstreetmap-carto/project.mml.patch
RUN patch project.mml project.mml.patch
# Generate the style
RUN carto project.mml > mapnik.xml

# Copy the entrypoint
COPY app.py /app/app.py
RUN chmod +x /app/app.py
ENTRYPOINT ["/app/app.py"]
