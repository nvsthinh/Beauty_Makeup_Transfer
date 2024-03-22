# Environmental Monitoring Fe


# Run frontend
install package: npm install
run app: 
npx expo start
a : open emulator
r : restart emulator

# Run backend
## Command connect database
docker run --name makeupStyle -e POSTGRES_PASSWORD=admin -p 5432:5432 -v D:\OutSource\Beauty_Makeup_Transfer\Beauty_Makeup_Transfer\data -d postgres