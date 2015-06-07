var name = "AlbERt EINstEiN";

function nameChanger(oldName) {
    var finalName = oldName;
    // Your code goes here!
    var space = ' ';
    words = finalName.split(space);
    firstLetter = words[0][0].toUpperCase();
    remainingLetters = words[0].slice(1).toLowerCase();
    lastWord = words[1].toUpperCase();
    
    finalName = firstLetter+remainingLetters+" "+lastWord ;

    // finalName = names.join(" ");
    
    // Don't delete this line!
    return finalName;
}

// Did your code work? The line below will tell you!
console.log(nameChanger(name));