	img_source = load("test3.png")
	new_width = 160
	percentage_scale = new_width / size(img_source,2);
	new_size = trunc.(Int, size(img_source) .* percentage_scale);
	img_t = imresize(img_source, new_size);
	img = Gray.(img_t)

    img_binary = binarize(img, Sauvola())

    # Use a weighted sum of rgb giving more weight to colors we perceive as 'brighter'
# Based on https://www.tutorialspoint.com/dip/grayscale_to_rgb_conversion.htm
brightness(c::AbstractRGB) = 0.3 * c.r + 0.59 * c.g + 0.11 * c.b

# ╔═╡ de4b9166-e44d-4886-b2c2-2f57a1d82d06
Gray.(brightness.(img))