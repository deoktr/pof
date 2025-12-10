/*
* This yara rules are designed to identify Python malware from their source code.
*/

rule execFunction
{
    meta:
        description = "Function `exec` used"
        author = "deoktr"

    strings:
        $exec = "exec"

    condition:
        any of them
}

rule suspiciousImports
{
    meta:
        description = "Suspicious library imports"
        author = "deoktr"

    strings:
        $base64 = "import base64"
        $base64from = "from base64 import b64decode"
        $base85 = "from base64 import b85decode"

    condition:
        any of them
}

// no comments
//rule noComments
//{
//    meta:
//        description = "No comments found"
//        author = "deoktr"
//
//    strings:
//        $comment = /#.{1,2}/
//
//    condition:
//        not any of them
//}

// obfuscation
rule obfuscationOxyry
{
    meta:
        description = "Obfuscation using Oxyry"
        author = "deoktr"
        resources = "https://pyob.oxyry.com/"

    strings:
        $varialbes = /O[O0]{16}/

    condition:
        all of them
}

// LOTL
rule LOTLURL
{
    meta:
        description = "Living Off Trusted Sites URLs"
        author = "deoktr"
        resources = "https://lots-project.com/"

    strings:
        // TODO (deoktr): complete the list
        $githubusercontent = "githubusercontent"
        $github = "github"
        $pastebin = "pastebin"

    condition:
        any of them
}

rule zerowidthspace
{
    meta:
        description = "Whitespace encoding with zero width spaces"
        author = "deoktr"

    strings:
        $a = "\xe2\x80\x8b"

    condition:
        any of them
}

// TODO
// single spaces indentation
// no newlines
// no docstrings
