from Package import Package
from Word import Word

#"youtube", "request", "openssl", "ssl", "cPickle", "python3", "git", "tkinter", "docker"

while True:
    word = input("insert package: ")
    print("----- checking package: " + word + " -----")
    word = Word(word)
    package = Package(word.value)
    if not package.exists:
        print("package does not exist")
    elif package.stars < 100:
        print("small number of stars ({})".format(package.stars))
    similar = word.similar_words
    all_similar_packages = [Package(word) for word in list(similar)[:20]]
    exists_similar_packages = [package for package in all_similar_packages if package.exists]
    better_choices = [sim_package for sim_package in exists_similar_packages if (not package or sim_package > package) and sim_package.stars > 100]
    better_choices_ordered = sorted(better_choices, key=lambda package: package.stars, reverse=True)
    if better_choices:
        print("please consider installing another package: " + str(better_choices_ordered))
    elif package.stars >= 100:
        print("{} is safe".format(package))
