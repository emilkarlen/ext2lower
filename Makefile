help:
	echo all clean
all: out out/ext2lower

clean:
	rm -rf out

out:
	mkdir out

out/ext2lower: src/ext2lower.py
	echo -n '#! '         > out/ext2lower
	which python3        >> out/ext2lower
	cat src/ext2lower.py >> out/ext2lower
	chmod +x out/ext2lower
