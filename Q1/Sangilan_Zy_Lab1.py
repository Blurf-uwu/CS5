t = float(input("temperature: "))
v = float(input("speed: "))

if float(t) < 10 and float(v) > 4.8:
    print(f'windchill: {round(13.12 + 0.6215*t - 11.37*v**0.16 + 0.3965 * t * v**0.16, 4)} °C')
else:
    print("I can't compute for the wind chill with the values you specified.")