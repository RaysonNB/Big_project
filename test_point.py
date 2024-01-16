ys1 = math.cos(d) * ys + math.sin(d) * xs
ys2 = math.cos(d) * ys - math.sin(d) * xs
if xs != 0:
    xs1 = (math.cos(d) * (xs ** 2 + ys ** 2) - ys * ys1) / xs
    xs2 = (math.cos(d) * (xs ** 2 + ys ** 2) - ys * ys2) / xs
else:
    xs1 = -1 * math.sqrt(ys ** 2 - ys1 ** 2)
    xs2 = math.sqrt(ys ** 2 - ys2 ** 2)
