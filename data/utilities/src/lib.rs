use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyString};

#[pyfunction]
/// Formats the sum of two numbers as string.
fn camel_space_case(text: &PyString) -> PyResult<String> {
    let mut _text: String = text.extract().unwrap();
    let mut n_string: String = "".to_string();
    let mut _s: String = '_'.to_string();  // Virtual separator.
    //  pyo3::ffi::PyObject_Print
    // https://doc.rust-lang.org/std/string/
    // push_str add str .len(); HashMap text.split_whitespace()
    /* clear pop remove(n) s.insert(0, 'f'); let mut s = String::with_capacity(3);
    // fancy_f.chars().count() !v.is_empty() find(x) v.is_empty()
    // v.get(1..).is_none() s.split_at(3) s.split_at_mut(3)
    // starts_with(x) contains(x) ends_with(x) rfind(x)
    .split_terminator(".")
    use std::fs::File;

fn main() {
    let f = File::open("hello.txt");
}
*/
    if !_text.contains(&_s) && _text.contains(' ') {
        _s = ' '.to_string();
    }
    // let space: char = ' ';
    
    for sep in _text.split(&_s) {
        
        if _text != "ot" {
            // sep.capitalize()
            n_string.push_str(sep);
            n_string.push(' ');
        } else {
            n_string.push_str("OT ");
        }
    }
    /*
    Chars
    .is_alphabetic() .is_numeric() .len_utf8() .len() is_lowercase() is_uppercase()
    .is_whitespace() .is_alphanumeric()
    */
    print!("{0} {1}\n", "a".sizeof(), "A".sizeof());
    Ok((n_string).to_string())
}


#[pymodule]
/// Script Name: utilities.py
/// Utilities for Open Translation.
fn utilities(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(camel_space_case))?;
    //m.add_class::<TzClass>()?;

    Ok(())
}