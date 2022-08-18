fn main() {
    use std::process::Command;

    let output = Command::new("python3")
                         .args(["../__main__.py", "-trs"])
                         .output()
                         .unwrap();
    let mut text = String::from_utf8(output.stdout).unwrap();
    println!("{}", text);
}