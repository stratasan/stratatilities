workflow "CI" {
    on = "push"
    resolves = [
        "lint"
    ]
}

action "test-27" {
    uses = "./actions/test-27"
}

action "test-27" {
    uses = "./actions/test-35"
}

action "test-27" {
    uses = "./actions/test-36"
}

action "test-27" {
    uses = "./actions/test-37"
}

action "lint" {
    uses = "./actions/lint"
}
