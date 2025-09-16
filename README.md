docker network create myNetwork

docker run --name booking_db `
    -p 6432:5432 `
    -e POSTGRES_USER=abcde `
    -e POSTGRES_PASSWORD=abcde `
    -e POSTGRES_DB=booking `
    --network myNetwork `
    --volume pg-booking-data:/var/lib/postgresql/data `
    -d postgres:17.6

docker run --name booking_cache `
    -p 7379:6379 `
    --network=myNetwork `
    -d redis:8.2.1


docker build -t booking_image .


docker run --name booking_nginx `
    --volume /root/project/nginx.conf:/etc/nginx/nginx.conf `
    --network=myNetwork `
    -d -p 80:80 nginx