'use strict';

var _test = require('test');

var assert = require('../node_modules/chai').assert; /**
                                                      * Created by kevin on 28/05/16.
                                                      */

var expect = require('../node_modules/chai').expect;
var supertest = require('../node_modules/supertest');

var api = supertest('http://localhost:5000');

describe('Endpoints', function () {
    describe('sku_detail', function () {
        it('should return a response of 200', function (done) {
            api.get('/reporting/api/v1.0/sku_detail').set('accept', 'application/json').expect(200, done);
        });
    });

    describe('sku_detail', function () {
        it('should return a response of 200', function (done) {
            api.get('/reporting/api/v1.0/sku_detail').set('accept', 'application/json').expect(200).end(function (err, res) {
                //console.log(res.body.json_list[0]);
                expect(res.body.json_list[0]).to.have.property("id");
                expect(res.body.json_list[0].average_orders).to.not.equal(null);
                expect(res.body.json_list[0]).to.have.property("classification");
                expect(res.body.json_list[0].classification).to.not.equal(null);
                done();
            });
        });
    });
});

//# sourceMappingURL=test-compiled.js.map

//# sourceMappingURL=test-compiled-compiled.js.map