from bson import ObjectId

ids = [
    "6725e5f9fcd87bab1fd43411",
    "6727726ffcd87bab1fd4cc8e",
    "671705bd0388eb1a4c865ade",
    "677bb55a04ec0976019bdfbe",
    "676bed99388c28a7e043a4a6",
    "671705bd0388eb1a4c865ade",
    "678146d1006accb326be548e",
    "678146d1006accb326be548e",
    "6717194b0388eb1a4c86600a",
    "6773690cf4449a79d803e3a4",
    "6727726ffcd87bab1fd4cc8e",
    "6773690cf4449a79d803e3a4",
    "677360aaf4449a79d803de10",
    "6781bbea006accb326be6dd6",
    "6781d6c82fdce827b3ae32e7",
    "6727726ffcd87bab1fd4cc8e",
    "6781eb1a2fdce827b3ae42ff",
    "6781eb1a2fdce827b3ae42ff",
    "671705bd0388eb1a4c865ade",
    "6781e8c22fdce827b3ae4183",
    "6773690cf4449a79d803e3a4",
    "6773690cf4449a79d803e3a4",
    "677d280bb6894ca622b2794f",
    "678161e2006accb326be5e48",
    "677d299fb6894ca622b27b27",
    "6781d6c82fdce827b3ae32e7",
]

object_ids = [ObjectId(id) for id in ids]
print(object_ids)
