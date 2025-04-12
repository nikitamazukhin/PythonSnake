# Use the official Python image as base
FROM python:3.10-slim as pygame_build

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory into the container
COPY . .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Build the web application for the game
RUN pygbag --build game

# Replace nginx index.html template with game
FROM nginx:latest
COPY --from=pygame_build /app/game/build/web/game.apk /usr/share/nginx/html
COPY --from=pygame_build /app/game/build/web/favicon.png /usr/share/nginx/html
COPY --from=pygame_build /app/game/build/web/index.html /usr/share/nginx/html/index.html
