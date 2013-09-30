#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import scraperwiki

URL = 'http://diplomovka.sme.sk/zoznam-skol-a-univerzit.php'

def _parse_href_name(pq_el):
    if pq_el.find('a'):
        return pq_el.find('a').text(), pq_el.find('a').attr('href')
    else:
        return pq_el.text(), None


doc = pq(url=URL)
data = {}

school_id = 1
faculty_id = 1
dep_id = 1

schools = doc.find('div.article > ul > li')
for one in schools:
    one = pq(one)
    school = one.find('strong')
    _school = school.text()
    data = { 'id': school_id, 'name': _school, 'url': school.find('a').attr('href') }
    scraperwiki.sqlite.save(['id'], data, table_name = 'school')
    for faculty in one.find('ul li'):
        faculty = pq(faculty)
        if not faculty.find('em'):
            continue
        _faculty = _parse_href_name(faculty.find('em'))
        data = { 'id': faculty_id, 'school_id' : school_id, 'name': _faculty[0], 'url': _faculty[1] }
        scraperwiki.sqlite.save(['id'], data, table_name = 'faculty')
        for dep in faculty.find('ul li'):
            dep = pq(dep)
            _dep = _parse_href_name(dep)
            data = { 'id': dep_id, 'school_id' : school_id, 'faculty_id' : faculty_id, 'name': _dep[0], 'url': _dep[1] }
            scraperwiki.sqlite.save(['id'], data, table_name = 'department')
            dep_id += 1
        faculty_id += 1
    school_id += 1#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import scraperwiki

URL = 'http://diplomovka.sme.sk/zoznam-skol-a-univerzit.php'

def _parse_href_name(pq_el):
    if pq_el.find('a'):
        return pq_el.find('a').text(), pq_el.find('a').attr('href')
    else:
        return pq_el.text(), None


doc = pq(url=URL)
data = {}

school_id = 1
faculty_id = 1
dep_id = 1

schools = doc.find('div.article > ul > li')
for one in schools:
    one = pq(one)
    school = one.find('strong')
    _school = school.text()
    data = { 'id': school_id, 'name': _school, 'url': school.find('a').attr('href') }
    scraperwiki.sqlite.save(['id'], data, table_name = 'school')
    for faculty in one.find('ul li'):
        faculty = pq(faculty)
        if not faculty.find('em'):
            continue
        _faculty = _parse_href_name(faculty.find('em'))
        data = { 'id': faculty_id, 'school_id' : school_id, 'name': _faculty[0], 'url': _faculty[1] }
        scraperwiki.sqlite.save(['id'], data, table_name = 'faculty')
        for dep in faculty.find('ul li'):
            dep = pq(dep)
            _dep = _parse_href_name(dep)
            data = { 'id': dep_id, 'school_id' : school_id, 'faculty_id' : faculty_id, 'name': _dep[0], 'url': _dep[1] }
            scraperwiki.sqlite.save(['id'], data, table_name = 'department')
            dep_id += 1
        faculty_id += 1
    school_id += 1